import asyncio
import io
import logging
import os
from itertools import starmap
from uuid import uuid4

import aiohttp
import chromadb
from chromadb.errors import NotFoundError
from fastapi import HTTPException, status
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from markitdown import MarkItDown
from pydantic import BaseModel, Field
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .db import crud
from .db.base import session_factory
from .schemas import AgentConfig, DocumentIn, DocumentOut
from .settings import CHECKPOINT_PATH, CHROMA_PATH, current_datetime, settings

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx"}
INDEX_NAME = "knowledge-index"

logger = logging.getLogger(__name__)

client = chromadb.PersistentClient(CHROMA_PATH)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=200, length_function=len
)


def convert_to_md(file_data: bytes, file_extension: str) -> str:
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(file_data), file_extension=file_extension)
    return result.text_content


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
)
async def get_embeddings(texts: list[str], batch_size: int = 10) -> list[list[float]]:
    """Векторизация текста.

    :param texts: Тексты, которые нужно векторизовать.
    :param batch_size: Количество текста векторизуемого за один запрос.
    :returns: Массив ембедингов.
    """

    logger.info("POST: `%s`", f"{settings.embeddings_base_url}/embeddings")
    timeout = aiohttp.ClientTimeout(total=120 * 5)
    headers = {"Content-Type": "application/json"}
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        async with aiohttp.ClientSession(
                base_url=settings.embeddings_base_url, timeout=timeout
        ) as session, session.post(
            url="/embeddings", json={"texts": batch_texts}, headers=headers
        ) as response:
            response.raise_for_status()
            data = await response.json()
            if data.get("embeddings") is None:
                raise ValueError("Missing embeddings value in JSON response!")
            batch_embeddings = data.get("embeddings", [])
            embeddings.extend(batch_embeddings)
    return embeddings


async def index_document(file_data: bytes, file_name: str, **extra_metadata) -> DocumentOut:
    """Индексация документа: конвертация в Markdown -> сохранение в БД ->
    разделение на чанки + векторизация -> добавление в векторную БД.

    :param file_data: Бинарный контент файла.
    :param file_name: Имя файла.
    :returns: Созданный экземпляр документа.
    :raises HTTPException: 406 неподдерживаемый тип файла, 500 ошибка векторизации
    """

    extension = f".{file_name.rsplit(".", maxsplit=1)[-1]}"
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File type not allowed!"
        )
    md_text = convert_to_md(file_data, extension)
    document_in = DocumentIn(file_name=file_name, md_text=md_text, extra_metadata=extra_metadata)
    try:
        async with session_factory() as session:
            document = await crud.create_document(session, document_in)
            collection = client.get_or_create_collection(INDEX_NAME)
            chunks = splitter.split_text(md_text)
            embeddings = await get_embeddings(chunks)
            metadata = {"document_id": document.id, "file_name": file_name, **extra_metadata}
            collection.add(
                ids=[str(uuid4()) for _ in range(len(chunks))],
                documents=chunks,
                embeddings=embeddings,
                metadatas=[metadata.copy() for _ in range(len(chunks))],
            )
            await session.commit()
    except (aiohttp.ClientError, ValueError):
        await session.rollback()
        logger.exception("Error occurred while indexing document")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while indexing document"
        ) from None
    return document


async def remove_document(document_id: int) -> None:
    """Полное удаление документа из всех источников"""

    collection = client.get_or_create_collection(INDEX_NAME)
    async with session_factory() as session:
        try:
            await crud.delete_document(session, document_id)
            collection.delete(where={"document_id": document_id})
        except NotFoundError:
            await session.rollback()
            logger.exception("Not found document in collection")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chunks not found"
            ) from None


def default_result_formatter(
        document: str, metadata: dict[str, str | float], distance: float
) -> str:
    """Дефолтная функция для форматирования результата поиска релевантных документов"""

    return (
        f"**Distance:** {round(distance, 2)}\n"
        f"**Title:** {metadata.get('title', '')}\n"
        f"**Source:** {metadata.get('source', '')}\n"
        f"**Category:** {metadata.get('category', '')}\n"
        "**Document:**\n"
        f"{document}"
    )


class SearchInput(BaseModel):
    """Входные аргументы для поиска информации в базе знаний"""

    query: str = Field(description="Запрос для поиска")


@tool(
    "search_knowledge",
    description="""\
    Выполняет поиск по базе знаний компании. Используй этот инструмент для ответа на
    вопросы пользователя.
    """,
    args_schema=SearchInput,
)
async def search_knowledge(query: str) -> str:
    collection = client.get_or_create_collection(INDEX_NAME)
    embeddings = await get_embeddings([query])
    result = collection.query(
        query_embeddings=embeddings, include=["documents", "metadatas", "distances"]
    )
    docs = list(
        starmap(
            default_result_formatter,
            zip(
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0],
                strict=False,
            ),
        )
    )
    return "\n\n".join(docs)


async def call_chatbot(session_id: str, message: str, config: AgentConfig) -> str:
    """Вызов AI чат-бота"""

    base_prompt = f"**Текущая дата и время:** {current_datetime()}"
    system_prompt = base_prompt + "\n\n" + config.system_prompt
    async with AsyncSqliteSaver.from_conn_string(os.fspath(CHECKPOINT_PATH)) as checkpointer:
        await checkpointer.setup()
        agent = create_agent(
            model=ChatOpenAI(
                api_key=settings.yandex_cloud_api_key,
                model=settings.get_model_uri(config.model_id),
                base_url=settings.yandex_cloud_base_url,
                temperature=config.temperature,
            ),
            system_prompt=system_prompt,
            tools=[search_knowledge],
            checkpointer=checkpointer,
        )
        result = await agent.ainvoke(
            {"messages": [("human", message)]},
            config={"configurable": {"thread_id": session_id}}
        )
        return result["messages"][-1].content

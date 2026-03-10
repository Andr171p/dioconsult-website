from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import crud
from ..dependencies import get_db
from ..schemas import Document
from ..service import index_document, remove_document

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=Document,
    summary="Загрузка документа в базу знаний",
)
async def upload_document(
        file: UploadFile = File(...),
        source: str | None = Form(default=None, description="Источник откуда взят документ"),
        title: str | None = Form(default=None, description="Главный заголовок"),
        category: str | None = Form(default=None, description="Категория или тип документа"),
        tags: str | None = Form(default=None, description="Теги через запятую"),
) -> Document:
    file_name = file.filename
    file_data = await file.read()
    return await index_document(
        file_data, file_name, title=title, source=source, category=category, tags=tags
    )


@router.get(
    path="/{document_id}",
    status_code=status.HTTP_200_OK,
    response_model=Document,
    summary="Получение документа по его ID"
)
async def get_document(document_id: int, session: AsyncSession = Depends(get_db)) -> Document:
    document = await crud.read_document(session, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.delete(
    path="/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление документа",
)
async def delete_document(document_id: int) -> None:
    return await remove_document(document_id)

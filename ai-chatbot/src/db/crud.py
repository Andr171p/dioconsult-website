from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import DocumentIn, DocumentOut
from .models import DocumentOrm


async def create_document(session: AsyncSession, document: DocumentIn) -> DocumentOut:
    """Запись документа в базу данных"""

    stmt = insert(DocumentOrm).values(**document.model_dump()).returning(DocumentOrm)
    result = await session.execute(stmt)
    model = result.scalar_one()
    return DocumentOut.model_validate(model)


async def read_document(session: AsyncSession, document_id: int) -> DocumentOut | None:
    """Чтение документа по его уникальному ID"""

    stmt = select(DocumentOrm).where(DocumentOrm.id == document_id)
    result = await session.execute(stmt)
    model = result.scalar_one_or_none()
    return None if model is None else DocumentOut.model_validate(model)


async def delete_document(session: AsyncSession, document_id: int) -> None:
    """Удаление документа по его уникальному ID"""

    stmt = delete(DocumentOrm).where(DocumentOrm.id == document_id)
    await session.execute(stmt)

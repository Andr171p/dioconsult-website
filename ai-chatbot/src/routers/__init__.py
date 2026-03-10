__all__ = ["router"]

from fastapi import APIRouter

from .chat import router as chat_router
from .documents import router as document_router

router = APIRouter(prefix="/api/v1")

router.include_router(chat_router)
router.include_router(document_router)

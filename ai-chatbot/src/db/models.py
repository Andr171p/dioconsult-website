from sqlalchemy import JSON, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DocumentOrm(Base):
    __tablename__ = "documents"

    file_name: Mapped[str]
    extension: Mapped[str]
    md_text: Mapped[str] = mapped_column(TEXT)
    extra_metadata: Mapped[dict[str, str | float]] = mapped_column(JSON)

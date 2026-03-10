from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, PositiveInt, computed_field

from .settings import AVAILABLE_MODELS


class DocumentIn(BaseModel):
    """Модель для создания документа"""

    file_name: str = Field(..., description="Оригинальное имя файла")
    md_text: str = Field(..., description="Контент в формате Markdown")
    extra_metadata: dict[str, str | float] = Field(
        default_factory=dict,
        description="Дополнительные параметры, которые нужно передать в контекст",
        examples=[{"source": "https://example.com", "category": "FAQ", "tags": "python, fastapi"}],
    )

    @computed_field(description="Расширение файла", examples=[".pdf", ".docx"])
    def extension(self) -> str:
        return f".{self.file_name.rsplit(".", maxsplit=1)[-1]}"


class DocumentOut(BaseModel):
    """Модель для чтения документа / API ответа"""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt = Field(..., description="ID загруженного документа")
    created_at: datetime = Field(..., description="Дата и время создания")
    file_name: str = Field(..., description="Оригинальное имя файла")
    extension: str = Field(..., description="Расширение файла", examples=[".pdf", ".docx"])
    md_text: str = Field(..., description="Контент в формате Markdown")
    extra_metadata: dict[str, str | float] = Field(
        default_factory=dict,
        description="Дополнительные параметры, которые нужно передать в контекст",
        examples=[{"source": "https://example.com", "category": "FAQ", "tags": "python, fastapi"}]
    )


class ChatInputs(BaseModel):
    """Запрос к чат-боту"""

    session_id: str = Field(..., description="ID текущей сессии (для сохранения истории диалога)")
    message: str = Field(..., description="Текст сообщения пользователя")
    page_url: str | None = Field(
        default=None, description="URL страницы, где находится пользователь"
    )


class ChatResponse(BaseModel):
    """Сгенерированный API ответ от чат-бота"""

    reply: str = Field(..., description="Ответ от AI")


class AgentConfig(BaseModel):
    """Конфигурация поведения чат-бота"""

    model_config = ConfigDict(from_attributes=True)

    llm_provider: str = Field(default="YandexCloud", description="Провайдер LLM модели")
    model_id: AVAILABLE_MODELS = Field(
        default="qwen3-235b-a22b-fp8/latest", description="Имя используемой модели"
    )
    temperature: NonNegativeFloat = Field(
        ...,
        description="Температура генерации (0.0 = детерминировано, 1.0+ = креативно)",
        ge=0.0,
        le=2.0,
    )
    system_prompt: str = Field(..., description="Системный промпт, задающий поведение")

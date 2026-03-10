import anyio
from fastapi import APIRouter, status

from ..schemas import ChatBotAsk, ChatBotConfig
from ..settings import CHATBOT_CONFIG_FILE

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post(
    path="/ask",
    status_code=status.HTTP_200_OK,
    response_model=...,
    summary="Сгенерировать ответ"
)
async def ask_chatbot(): ...


@router.get(
    path="/config",
    status_code=status.HTTP_200_OK,
    response_model=ChatBotConfig,
    summary="Получение текущей конфигурации"
)
async def get_config() -> ChatBotConfig:
    json_data = await anyio.Path(CHATBOT_CONFIG_FILE).read_text(encoding="utf-8")
    return ChatBotConfig.model_validate_json(json_data)


@router.put(
    path="/config",
    status_code=status.HTTP_201_CREATED,
    summary="Редактирование конфигурации",
)
async def edit_config(config: ChatBotConfig) -> None:
    await anyio.Path(CHATBOT_CONFIG_FILE).write_text(config.model_dump_json())

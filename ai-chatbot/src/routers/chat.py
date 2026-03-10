import anyio
from fastapi import APIRouter, Depends, status

from ..dependencies import get_agent_config
from ..schemas import AgentConfig, ChatInputs, ChatResponse
from ..service import call_chatbot
from ..settings import AGENT_CONFIG_FILE

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    path="/completions",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
    summary="Генерация ответа"
)
async def generate_response(
        inputs: ChatInputs, config: AgentConfig = Depends(get_agent_config)
) -> ChatResponse:
    response_text = await call_chatbot(
        session_id=inputs.session_id, message=inputs.message, config=config
    )
    return ChatResponse(reply=response_text)


@router.get(
    path="/config",
    status_code=status.HTTP_200_OK,
    response_model=AgentConfig,
    summary="Получение текущей конфигурации чат-бота"
)
async def get_config(config: AgentConfig = Depends(get_agent_config)) -> AgentConfig:
    return config


@router.put(
    path="/config",
    status_code=status.HTTP_201_CREATED,
    summary="Редактирование конфигурации чат-бота",
)
async def edit_config(config: AgentConfig) -> None:
    await anyio.Path(AGENT_CONFIG_FILE).write_text(config.model_dump_json())

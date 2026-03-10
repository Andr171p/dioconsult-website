import anyio
from sqlalchemy.ext.asyncio import AsyncSession

from .db.base import session_factory
from .schemas import AgentConfig
from .settings import AGENT_CONFIG_FILE


async def get_db() -> AsyncSession:
    async with session_factory() as session:
        yield session


async def get_agent_config() -> AgentConfig:
    json_data = await anyio.Path(AGENT_CONFIG_FILE).read_text(encoding="utf-8")
    return AgentConfig.model_validate_json(json_data)

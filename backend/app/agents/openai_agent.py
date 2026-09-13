import os

from agents import Agent, Runner

from app.agents.base import BaseAgent
from app.core.config import settings


class OpenAIAgent(BaseAgent):
    """基于 OpenAI Agents SDK 的智能体。

    底层使用 OPENAI_API_KEY / OPENAI_BASE_URL 环境变量，这里在实例化时注入。
    """

    name = "openai-agents"
    description = "基于 OpenAI Agents SDK 的智能体"

    def __init__(self) -> None:
        os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)
        if settings.OPENAI_BASE_URL:
            os.environ.setdefault("OPENAI_BASE_URL", settings.OPENAI_BASE_URL)
        self.agent = Agent(
            name="assistant", instructions="You are a helpful assistant."
        )

    async def run(self, prompt: str, **kwargs) -> str:
        result = await Runner.run(self.agent, prompt)
        return result.final_output

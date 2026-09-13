from app.agents.base import BaseAgent
from app.core.llm import get_chat_model


class LangChainAgent(BaseAgent):
    """基于 LangChain + ChatOpenAI 的简单对话智能体。"""

    name = "langchain"
    description = "基于 LangChain + ChatOpenAI 的简单对话智能体"

    def __init__(self, provider: str = "openai", **model_kwargs) -> None:
        # 模型连接统一由 core.llm 工厂提供，agent 不再关心密钥/地址
        self.llm = get_chat_model(provider=provider, **model_kwargs)

    async def run(self, prompt: str, **kwargs) -> str:
        result = await self.llm.ainvoke(prompt)
        return result.content

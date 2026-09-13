from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """智能体统一抽象接口。

    所有智能体实现（LangChain / LangGraph / OpenAI Agents）都应继承此类，
    保证上层服务可以无差别地调用。
    """

    name: str = "base"
    description: str = ""

    @abstractmethod
    async def run(self, prompt: str, **kwargs) -> str:
        """执行一次智能体调用，返回文本结果。"""
        raise NotImplementedError

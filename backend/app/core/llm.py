"""LLM 客户端工厂。

把「模型怎么连」与「模型怎么用」解耦：所有 agent 都从这里取聊天模型，
新增 provider（Anthropic / 本地模型）只需在此扩展，不用改 agent 代码。

设计原则（与 database.py / redis.py 一致）：
- core 只负责「对外部服务的连接封装」
- 不在这里写任何业务规则，也不关心 agent 怎么编排
"""
from __future__ import annotations

from app.core.config import settings


def get_chat_model(provider: str = "openai", **overrides) -> object:
    """构造一个聊天模型客户端。

    Args:
        provider: 模型提供商，目前支持 "openai"。
        **overrides: 覆盖默认参数（如 model="gpt-4o-mini", temperature=0）。

    Returns:
        LangChain 兼容的 ChatModel 实例（支持 .invoke / .ainvoke）。
    """
    provider = (provider or "openai").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        params = {
            "model": settings.OPENAI_MODEL,
            "api_key": settings.OPENAI_API_KEY,
            "base_url": settings.OPENAI_BASE_URL,
            "temperature": 0.7,
        }
        params.update(overrides)
        return ChatOpenAI(**params)

    # 未来扩展点（在 config.py 增加对应密钥即可）：
    # if provider == "anthropic":
    #     from langchain_anthropic import ChatAnthropic
    #     return ChatAnthropic(model=settings.ANTHROPIC_MODEL,
    #                          api_key=settings.ANTHROPIC_API_KEY)
    # if provider == "local":
    #     from langchain_openai import ChatOpenAI
    #     return ChatOpenAI(model=settings.LOCAL_MODEL,
    #                       api_key="not-needed",
    #                       base_url=settings.LOCAL_BASE_URL)

    raise ValueError(f"Unsupported LLM provider: {provider}")

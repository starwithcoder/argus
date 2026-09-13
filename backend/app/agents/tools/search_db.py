"""示例工具：在业务库中检索并聚合记录。

演示「tool 调用 service 层」的正确姿势——tool 本身不写 ORM，而是委托给
services/ 里的业务逻辑，保持分层清晰。

占位阶段仅给出签名与文档，接入时把 TODO 替换为真实 service 调用。
"""
from __future__ import annotations

from typing import Any


async def search_db_tool(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """在业务库中检索匹配记录。

    Args:
        query: 检索关键词。
        limit: 返回条数上限。

    Returns:
        匹配记录列表。

    TODO: 改为调用 service 层，例如::

        from app.services import search_service
        return await search_service.search(query, limit)
    """
    raise NotImplementedError("search_db_tool 待接入 service 层")

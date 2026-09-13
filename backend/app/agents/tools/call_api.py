"""示例工具：调用外部 HTTP 接口。

供智能体在推理过程中访问第三方服务（如天气、搜索、内部 API）。
"""
from __future__ import annotations

import httpx


async def call_api_tool(url: str, method: str = "GET", **kwargs) -> str:
    """调用外部 HTTP 接口并返回文本响应。

    Args:
        url: 目标地址。
        method: HTTP 方法（GET / POST / ...）。
        **kwargs: 透传给 httpx 的额外参数（如 json=..., params=...）。

    Returns:
        响应文本内容。
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp.text

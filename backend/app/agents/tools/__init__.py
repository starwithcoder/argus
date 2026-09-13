"""智能体工具（function calling tools）。

每个 tool 是智能体的一项「能力」。tool 内部通常调用 services/ 或 core/，
避免把业务规则直接写在 agent 里。

新增工具：在本目录新建一个模块，实现一个 async 函数，再在此处导出即可。
"""
from app.agents.tools.call_api import call_api_tool
from app.agents.tools.search_db import search_db_tool

__all__ = ["search_db_tool", "call_api_tool"]

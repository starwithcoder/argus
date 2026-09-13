"""MCP（Model Context Protocol）客户端：连接「百度搜索」MCP server。

本模块属于框架无关的基础设施层（core），职责只有三件事：
1. 与 MCP server 建立传输连接（stdio 拉起子进程 / SSE 连接远程服务）
2. 自动发现并缓存 server 暴露的 tools
3. 把「百度搜索」封装成一个易用的 search() 方法

具体工具怎么被智能体编排使用，交给 app/agents/*，这里不写任何业务逻辑。

依赖：官方 MCP Python SDK（pip install mcp）。为避免无该依赖时 core 包导入失败，
      所有 mcp 相关导入都放在方法内部（懒加载）。
"""

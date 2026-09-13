from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.base import BaseAgent
from app.core.llm import get_chat_model


class AgentState(TypedDict):
    input: str
    output: str


class LangGraphWorkflow(BaseAgent):
    """基于 LangGraph 的多步骤工作流（占位骨架）。

    当前为单节点示例，后续可扩展为「检索 -> 推理 -> 工具调用」多节点图。
    """

    name = "langgraph"
    description = "基于 LangGraph 的多步骤工作流（占位）"

    def __init__(self, provider: str = "openai", **model_kwargs) -> None:
        self.llm = get_chat_model(provider=provider, **model_kwargs)
        self._graph = self._build()

    def _build(self):
        def call_model(state: AgentState) -> AgentState:
            msg = self.llm.invoke(state["input"])
            return {"input": state["input"], "output": msg.content}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", call_model)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)
        return workflow.compile()

    async def run(self, prompt: str, **kwargs) -> str:
        result = await self._graph.ainvoke({"input": prompt, "output": ""})
        return result["output"]

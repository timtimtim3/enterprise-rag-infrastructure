from typing import Literal

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agents.agent_node import AgentNode
from app.agents.state import AgentState
from app.agents.tools import build_agent_tools


MAX_TOOL_ITERATIONS = 6


def build_agent_graph(llm, retriever):
    tools = build_agent_tools(retriever)

    agent_node = AgentNode(
        llm=llm,
        tools=tools,
    )

    tool_node = ToolNode(
        tools,
        handle_tool_errors=True,
    )

    async def execute_tools(state: AgentState):
        last_message = state["messages"][-1]

        # Keep some simple observability/history ourselves
        history = [
            {
                "tool": tool_call["name"],
                "args": tool_call["args"],
            }
            for tool_call in last_message.tool_calls
        ]

        result = await tool_node.ainvoke(state)

        return {
            "messages": result["messages"],
            "tool_iterations": 1,
            "tool_history": history,
        }

    def route_after_agent(
        state: AgentState,
    ) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]

        if not isinstance(last_message, AIMessage):
            return END

        # No tool call = model has produced its final answer
        if not last_message.tool_calls:
            return END

        # Safety guard
        if state.get("tool_iterations", 0) >= MAX_TOOL_ITERATIONS:
            return END

        return "tools"

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", execute_tools)

    graph.add_edge(START, "agent")

    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge("tools", "agent")

    return graph.compile()

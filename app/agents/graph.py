from typing import Literal

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage

from app.rag.helpers import format_sources_with_registry
from app.agents.agent_node import AgentNode
from app.agents.state import AgentContext, AgentState
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

        history = [
            {
                "tool": tool_call["name"],
                "args": tool_call["args"],
            }
            for tool_call in last_message.tool_calls
        ]

        result = await tool_node.ainvoke(state)

        source_registry = state.get(
            "source_registry",
            {},
        )

        processed_messages = []

        for message in result["messages"]:

            # Leave normal tools alone
            if (
                not isinstance(message, ToolMessage)
                or message.name != "search_company_knowledge"
            ):
                processed_messages.append(message)
                continue

            artifact = message.artifact or {}

            # Nothing retrieved
            if artifact.get("status") != "found":
                processed_messages.append(message)
                continue

            all_docs = artifact.get("all_docs", {})

            (
                formatted_context,
                source_registry,
                sources_this_call,
            ) = format_sources_with_registry(
                all_docs=all_docs,
                source_registry=source_registry,
            )

            processed_message = message.model_copy(
                update={
                    # What the LLM sees
                    "content": formatted_context,

                    # Structured data your backend keeps
                    "artifact": {
                        **artifact,
                        "sources": sources_this_call,
                    },
                }
            )

            processed_messages.append(processed_message)

        return {
            "messages": processed_messages,
            "tool_iterations": 1,
            "tool_history": history,
            "source_registry": source_registry,
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

    graph = StateGraph(
        state_schema=AgentState,
        context_schema=AgentContext,
    )
    
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

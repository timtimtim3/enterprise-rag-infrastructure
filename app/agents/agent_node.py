import json

from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    convert_to_openai_messages,
)
from langchain_core.utils.function_calling import convert_to_openai_tool

from app.agents.state import AgentState
from app.prompts.assistant.agent import AGENT_SYSTEM_PROMPT


class AgentNode:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

        self.tool_schemas = [
            convert_to_openai_tool(tool)
            for tool in tools
        ]

    async def __call__(self, state: AgentState):
        messages = [
            SystemMessage(content=AGENT_SYSTEM_PROMPT),
            *state["messages"],
        ]

        # LiteLLM expects OpenAI-style message dictionaries
        llm_messages = convert_to_openai_messages(messages)

        response = await self.llm.get_response(
            messages=llm_messages,
            tools=self.tool_schemas,
            temperature=0,
        )

        response_message = response.choices[0].message

        tool_calls = []

        for tool_call in response_message.tool_calls or []:
            arguments = tool_call.function.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            tool_calls.append(
                {
                    "name": tool_call.function.name,
                    "args": arguments,
                    "id": tool_call.id,
                    "type": "tool_call",
                }
            )

        message = AIMessage(
            content=response_message.content or "",
            tool_calls=tool_calls,
        )

        usage = response.usage

        return {
            "messages": [message],
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason,
        }
    
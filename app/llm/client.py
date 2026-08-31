from typing import Any

from litellm import acompletion


class LLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def get_response(
        self,
        messages: list[dict[str, Any]],
        temperature: float | None = None,
        tools: list[dict[str, Any]] | None = None,
    ):
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "tools": tools,
        }

        if self.model_name.startswith("openai/gpt-5.6"):
            kwargs["reasoning_effort"] = "none"

        return await acompletion(**kwargs)
    
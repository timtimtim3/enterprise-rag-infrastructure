from typing import Dict, List

from litellm import acompletion


class LLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def get_response(self, messages: List[Dict[str, str]], temperature: float | None = None):
        # messages=[{"content": "Hello, how are you?", "role": "user"}]
        response = await acompletion(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        return response

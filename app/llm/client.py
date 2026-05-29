from typing import Dict, List

from litellm import completion


class LLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def get_response(self, messages: List[Dict[str, str]]):
        # messages=[{"content": "Hello, how are you?", "role": "user"}]
        response = completion(
            model=self.model_name,
            messages=messages
        )
        return response

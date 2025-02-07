from typing import Iterator, List, Dict
from .llm_provider import LLMProvider
import openai

class OpenAIProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str):
        openai.api_key = api_key
        openai.api_base = base_url

    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float, ctx_size: int) -> Iterator[str]:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        for chunk in completion:
            if 'choices' in chunk:
                yield chunk.choices[0].delta.get("content", "")

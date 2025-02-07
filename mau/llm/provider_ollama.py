from typing import Iterator, List, Dict
from .llm_provider import LLMProvider
import ollama

class OllamaProvider(LLMProvider):
    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float, ctx_size: int) -> Iterator[str]:
        response_stream = ollama.chat(
            model=model,
            messages=messages,
            options={"num_ctx": ctx_size, "temperature": temperature},
            stream=True,
        )
        for chunk in response_stream:
            yield chunk["message"]["content"]

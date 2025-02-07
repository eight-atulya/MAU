# mau/llm/provider_lmstudio.py
from typing import Iterator, List, Dict
from .llm_provider import LLMProvider
import openai

class LMStudioProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str, stream: bool = False):
        # Set stream=False by default for conversation mode.
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)
        self.stream = stream

    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float, ctx_size: int) -> Iterator[str]:
        # Use non-streaming mode if self.stream is False.
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=self.stream  # This will be False for conversation mode.
        )
        if self.stream:
            # If streaming is enabled, yield token-by-token.
            for chunk in completion:
                if "message" in chunk:
                    yield chunk["message"]["content"]
        else:
            # Non-streaming: yield the complete response as one token.
            yield completion.choices[0].message.content

from copy import deepcopy
from typing import Iterator, List, Dict, Optional
from .llm_provider import LLMProvider

class AIBeing:
    def __init__(
        self,
        name: str,
        model: str,
        temperature: float,
        ctx_size: int,
        system_prompt: str,
        provider: LLMProvider,
    ):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.ctx_size = ctx_size
        self.provider = provider
        self._messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    @property
    def messages(self) -> List[Dict[str, str]]:
        return deepcopy(self._messages)

    @property
    def system_prompt(self) -> str:
        return self._messages[0]["content"]

    @system_prompt.setter
    def system_prompt(self, value: str):
        self._messages[0]["content"] = value

    def add_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def chat(self, user_input: Optional[str] = None) -> Iterator[str]:
        if user_input is not None:
            self.add_message("user", user_input)
        response_chunks = []
        for chunk in self.provider.chat(self.model, self._messages, self.temperature, self.ctx_size):
            response_chunks.append(chunk)
            yield chunk
        self.add_message("assistant", "".join(response_chunks).strip())

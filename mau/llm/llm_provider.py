from abc import ABC, abstractmethod
from typing import Iterator, List, Dict

class LLMProvider(ABC):
    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float, ctx_size: int) -> Iterator[str]:
        """
        Run the chat API call and yield response chunks.
        """
        pass

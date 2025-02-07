import json
from dataclasses import dataclass, field
from typing import Iterator, List, Dict, TypedDict

from mau.llm.ai_being import AIBeing

class ConversationLogItem(TypedDict):
    agent: str
    content: str

@dataclass
class ConversationManager:
    agent1: AIBeing
    agent2: AIBeing
    initial_message: str | None
    use_markdown: bool = False
    allow_termination: bool = False
    _conversation_log: List[ConversationLogItem] = field(default_factory=list, init=False)

    def __post_init__(self):
        # Append extra instructions based on settings to the system prompts.
        instruction = ""
        if self.use_markdown:
            instruction += "\n\nYou may use Markdown formatting."
        if self.allow_termination:
            instruction += "\n\nYou may end the conversation by outputting `<TERMINATE>`."
        self.agent1.system_prompt += instruction
        self.agent2.system_prompt += instruction

    def run_conversation(self) -> Iterator[tuple[str, Iterator[str]]]:
        last_message = self.initial_message
        is_agent1_turn = True

        # If an initial message is provided, let agent1 start.
        if self.initial_message is not None:
            self.agent1.add_message("assistant", self.initial_message)
            self._conversation_log.append({"agent": self.agent1.name, "content": self.initial_message})
            yield (self.agent1.name, iter([self.initial_message]))
            is_agent1_turn = False

        while True:
            current_agent = self.agent1 if is_agent1_turn else self.agent2
            response_stream = current_agent.chat(last_message)
            last_message_chunks = []

            def stream_chunks() -> Iterator[str]:
                for chunk in response_stream:
                    last_message_chunks.append(chunk)
                    yield chunk

            yield (current_agent.name, stream_chunks())
            last_message = "".join(last_message_chunks).strip()
            self._conversation_log.append({"agent": current_agent.name, "content": last_message})
            if self.allow_termination and "<TERMINATE>" in last_message:
                break
            is_agent1_turn = not is_agent1_turn

    def save_conversation(self, filename: str):
        # Existing text file saving method.
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== Agent 1: {self.agent1.name} ===\n")
            f.write(f"Model: {self.agent1.model}\n")
            f.write(f"System Prompt: {self.agent1.system_prompt}\n\n")
            f.write(f"=== Agent 2: {self.agent2.name} ===\n")
            f.write(f"Model: {self.agent2.model}\n")
            f.write(f"System Prompt: {self.agent2.system_prompt}\n\n")
            f.write("=== Conversation Log ===\n")
            for msg in self._conversation_log:
                f.write(f"{msg['agent']}: {msg['content']}\n")

    def save_conversation_json(self, filename: str):
        # New method to save the conversation in JSON format.
        data = {
            "agent1": {
                "name": self.agent1.name,
                "model": self.agent1.model,
                "system_prompt": self.agent1.system_prompt,
            },
            "agent2": {
                "name": self.agent2.name,
                "model": self.agent2.model,
                "system_prompt": self.agent2.system_prompt,
            },
            "conversation": self._conversation_log
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

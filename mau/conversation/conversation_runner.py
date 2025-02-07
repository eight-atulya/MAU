import logging
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.markdown import Markdown
from mau.conversation.conversation_manager import ConversationManager
from mau.llm.ai_being import AIBeing
from mau.llm import provider_ollama, provider_openai, provider_lmstudio

logger = logging.getLogger(__name__)
console = Console()

def choose_provider(provider_name: str, provider_config: dict = None):
    provider_config = provider_config or {}
    if provider_name.lower() == "ollama":
        return provider_ollama.OllamaProvider()
    elif provider_name.lower() == "openai":
        base_url = provider_config.get("base_url", "https://api.openai.com/v1")
        api_key = provider_config.get("api_key", "")
        return provider_openai.OpenAIProvider(base_url, api_key)
    elif provider_name.lower() == "lmstudio":
        base_url = provider_config.get("base_url", "http://localhost:1234/v1")
        api_key = provider_config.get("api_key", "")
        # For conversation mode, we disable streaming.
        return provider_lmstudio.LMStudioProvider(base_url, api_key, stream=False)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


def run_conversation_mode(config: dict):
    # Create agents from config
    agent1_conf = config["agent1"]
    agent2_conf = config["agent2"]
    settings = config["settings"]

    provider1 = choose_provider(agent1_conf["provider"], agent1_conf.get("provider_config"))
    provider2 = choose_provider(agent2_conf["provider"], agent2_conf.get("provider_config"))

    agent1 = AIBeing(
        name=agent1_conf["name"],
        model=agent1_conf["model"],
        temperature=agent1_conf.get("temperature", 0.8),
        ctx_size=agent1_conf.get("ctx_size", 2048),
        system_prompt=agent1_conf["system_prompt"],
        provider=provider1,
    )

    agent2 = AIBeing(
        name=agent2_conf["name"],
        model=agent2_conf["model"],
        temperature=agent2_conf.get("temperature", 0.8),
        ctx_size=agent2_conf.get("ctx_size", 2048),
        system_prompt=agent2_conf["system_prompt"],
        provider=provider2,
    )

    manager = ConversationManager(
        agent1=agent1,
        agent2=agent2,
        initial_message=settings.get("initial_message"),
        use_markdown=settings.get("use_markdown", False),
        allow_termination=settings.get("allow_termination", False)
    )

    console = Console()
    console.print("[bold cyan]=== Conversation Started ===\n[/bold cyan]")
    try:
        for agent_name, message_stream in manager.run_conversation():
            console.print(f"[bold magenta]{agent_name}:[/bold magenta]", end=" ")
            for chunk in message_stream:
                console.print(chunk, end="")
            console.print("\n" + "-" * 80)
    except KeyboardInterrupt:
        console.print("\n[bold red]Conversation interrupted by user.[/bold red]")

    console.print("\n[bold cyan]=== Conversation Ended ===[/bold cyan]")

    save = prompt("Save conversation as JSON? (y/N): ").strip().lower()
    if save in ("y", "yes"):
        filename = prompt("Enter JSON filename (e.g., conversation.json): ").strip()
        manager.save_conversation_json(filename)
        console.print(f"Conversation saved to {filename} in JSON format.")

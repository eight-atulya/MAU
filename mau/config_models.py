from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class ProviderConfig(BaseModel):
    base_url: Optional[str] = None
    api_key: Optional[str] = None

class AgentConfig(BaseModel):
    name: str
    provider: str
    model: str
    system_prompt: str
    temperature: float = Field(default=0.8, ge=0.0, le=1.0)
    ctx_size: int = Field(default=2048, ge=0)
    provider_config: Optional[ProviderConfig] = None

class ConversationSettings(BaseModel):
    use_markdown: bool = False
    allow_termination: bool = False
    initial_message: Optional[str] = None

class ConversationConfig(BaseModel):
    agent1: AgentConfig
    agent2: AgentConfig
    settings: ConversationSettings
    pass

class DataPipelineConfig(BaseModel):
    layer_001_input_path: str
    output_dir_md: str
    output_dir_excel: str
    identity_prompt_path: str
    task_prompt_path: str
    provider: str
    provider_config: Optional[ProviderConfig] = None
    model: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    pass


class DataPipelineLayer1Config(BaseModel):
    identity_dir: str
    task_dir: str
    output_dir_md: str
    output_dir_excel: str
    identity_prompt_file: str
    task_prompt_file: str
    model: str
    provider_config: Dict[str, str]


class MAUConfig(BaseModel):
    conversation: ConversationConfig
    data_pipeline: DataPipelineConfig
    data_pipeline_layer1: DataPipelineLayer1Config
    output_formats: List[str]

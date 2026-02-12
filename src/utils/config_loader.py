import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Dict

class AppConfig(BaseModel):
    name: str
    debug: bool

class DatabaseConfig(BaseModel):
    path: str

class BotSettings(BaseModel):
    reply_interval: int
    max_daily_replies: int
    session_timeout: int

class AISettings(BaseModel):
    model_name: str
    temperature: float
    top_p: float

class PersonaConfig(BaseModel):
    active_persona: str
    definitions: Dict[str, str]

class RootConfig(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    bot_settings: BotSettings
    ai_settings: AISettings
    personas: PersonaConfig

def load_config(config_path: str = "config/settings.yaml") -> RootConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(path, "r") as f:
        config_data = yaml.safe_load(f)
    
    return RootConfig(**config_data)
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    PROJECT_VERSION: str = "0.1.1"
    API_V1_STR: str = "/api/v1"

    # API Security
    API_KEY: SecretStr
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
    
    # Pricing per 1M tokens (Example for Gemini 1.5 Flash)
    COST_PER_1M_INPUT_TOKENS: float = 0.075 
    COST_PER_1M_OUTPUT_TOKENS: float = 0.30
    
    # Simple Guardrail Config
    BANNED_KEYWORDS: list[str] = ["internal_password", "secret_key_123", "competitor_x"]

settings = Settings()
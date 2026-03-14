from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    PROJECT_VERSION: str = "0.1.1"
    API_V1_STR: str = "/api/v1"


    # --- NEW: Google Config ---
    GOOGLE_API_KEY: SecretStr
    GOOGLE_PROJECT_ID: str = ""

    # API Security
    API_KEY: SecretStr
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # --- NEW: Admin & Auth ---
    ADMIN_USER: str = "admin"
    ADMIN_PASSWORD: SecretStr  # Using SecretStr for better security
    
    # --- NEW: LLM Cost Tracking ---
    COST_PER_1M_INPUT_TOKENS: float = 0.075
    COST_PER_1M_OUTPUT_TOKENS: float = 0.30
    
    # --- NEW: Infrastructure & Logging ---
    LOG_FILE_PATH: str = "logs/app.log"
    QDRANT_HOST: str = "localhost"

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
    
    # Simple Guardrail Config
    BANNED_KEYWORDS: list[str] = ["internal_password", "secret_key_123", "competitor_x"]

settings = Settings()
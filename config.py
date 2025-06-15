from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ThumbScore AI"
    VERSION: str = "1.0.0"
    
    # Configurações do servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Configurações de ML
    MODEL_PATH: str = "ml/models/"
    MAX_IMAGE_SIZE: int = 1024 * 1024 * 5  # 5MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/webp"]
    
    # Configurações do OpenAI (GPT-4 Vision)
    OPENAI_API_KEY: Optional[str] = None
    GPT_MODEL: str = "gpt-4-vision-preview"
    MAX_TOKENS: int = 500
    
    # Configurações de cache
    CACHE_TTL: int = 3600  # 1 hora
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    
    # Configurações de CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()


import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # API Configuration
    api_title: str = "AI Flashcard Generator API"
    api_description: str = "Generate educational flashcards from text using AI"
    api_version: str = "1.0.0"
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load from environment if not provided
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

settings = Settings()

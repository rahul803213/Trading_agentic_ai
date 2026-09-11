from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://agent_user:agent_pass@localhost:5432/agent_db")
    
    # LLM
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # App
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    app_name: str = "Trade Behavioral Agent"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

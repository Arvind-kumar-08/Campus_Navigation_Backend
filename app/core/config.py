
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):

    DATABASE_URL: str
    GEMINI_API_KEY: str
    GROQ_API_KEY: str
    APP_NAME: str = "RGIPT Campus RAG Backend"

    APP_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
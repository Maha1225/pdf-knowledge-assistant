from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PDF Knowledge Assistant"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    upload_dir: str = "storage/uploads"

    chunk_size: int = 400
    chunk_overlap: int = 50
    top_k: int = 6

    openai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

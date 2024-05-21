from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV_TYPE: str
    IS_DEBUG: bool
    MPD_SERVER_IP: str
    MPD_SERVER_PORT: int
    UI_OPTION_SHORT_FILE_NAME: bool
    UI_OPTION_SHORT_FILE_LENGTH: int
    FILE_OPTION_UPLOAD_LIMIT_MB: int

    model_config = SettingsConfigDict(
        # Load .env first
        env_file=('.env.sample', '.env')
    )


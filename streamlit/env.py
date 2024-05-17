from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV_TYPE: str
    URL_BACKEND: str
    IS_DEBUG: bool
    UI_OPTION_TITLE: str
    UI_OPTION_DESC: str
    UI_OPTION_SIDEBAR_WIDTH: int
    TAG_DATE_BEGIN: int
    TAG_TARCK_END: int
    TAG_OPTION_WHIP: bool
    TAG_OPTION_MOVE_SOURCE_TO_TARGET: bool
    TAG_OPTION_MOVE_TARGET_TO_SOURCE: bool
    TAG_OPTION_MPD_UPDATE: bool


    model_config = SettingsConfigDict(
        env_file=('.env.sample', '.env')
    )


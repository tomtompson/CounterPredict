from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    RATE_LIMITING_ENABLE: bool = False
    RATE_LIMITING_FREQUENCY: str = "2/3seconds"
    FLARESOLVERR_HOST: str = "localhost"
    FLARESOLVERR_PORT: int = 8191
    TELEGRAM_BOT_TOKEN: str = "8650485388:AAHZ7X-dQmNfju7kkB_uHmb6voKWa-Bn3fU"
    TELEGRAM_CHAT_ID: str = "1418970711"

    @computed_field
    @property
    def FLARESOLVERR_URL(self) -> str:
        return f"http://{self.FLARESOLVERR_HOST}:{self.FLARESOLVERR_PORT}/v1"


settings = Settings()

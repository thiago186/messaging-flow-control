from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug_level: str = "INFO"
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone: str

    class Config:
        env_file = ".env"


settings = Settings()
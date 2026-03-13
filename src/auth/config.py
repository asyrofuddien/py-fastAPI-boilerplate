from pydantic import BaseSettings
from src.config import settings


class AuthConfig(BaseSettings):
    JWT_SECRET: str = settings.JWT_SECRET
    JWT_ALGORITHM: str = settings.JWT_ALGORITHM
    JWT_EXPIRATION_HOURS: int = settings.JWT_EXPIRATION_HOURS


auth_settings = AuthConfig()
import os
from pydantic_settings import BaseSettings
from typing import Optional


def get_secret(secret_name, default):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return os.getenv(secret_name, default)


class ConfigClass(BaseSettings):
    SECRET_KEY: str = get_secret("SECRET_KEY", 'H5zQCLkaY4d8hExSjghGyaJMm7XtCKNsab88JDy12M')
    ALGORITHM: str = get_secret("ALGORITHM", 'HS256')

    ADMIN_KEY: str = get_secret("ADMIN_KEY", "EpursaKey2024")
    API_KEY: str = get_secret("API_KEY", "AMC25Gva6pTEouh60ZDfKCZxCHfHJn-x-WoYPpoGRWQ")
    ADMIN_USERNAME: str = get_secret("ADMIN_USERNAME", "epursa")
    ADMIN_PASSWORD: str = get_secret("ADMIN_PASSWORD", "q6lr0tZXiX")

    # 60 minutes * 24 hours * 355 days = 365 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_secret("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 365))

    SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL",
                                              'postgresql://postgres:postgres19J2140@localhost:5432'
                                              '/auth_epursa')

    SQLALCHEMY_POOL_SIZE: int = 100
    SQLALCHEMY_MAX_OVERFLOW: int = 0
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = get_secret("SQLALCHEMY_POOL_RECYCLE", 3600)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
    }

    PREFERRED_LANGUAGE: str = get_secret("PREFERRED_LANGUAGE", 'fr')

    API_STR: str = get_secret("API_STR", "/api/v1/authentication")

    PROJECT_NAME: str = get_secret("PROJECT_NAME", "EPURSA AUTHENTICATION API")
    PROJECT_VERSION: str = get_secret("PROJECT_VERSION", "1.0.0")
    STORAGE_API_URL: str = get_secret("STORAGE_API_URL", "http://45.130.104.46:5008/api/v1/storage")
    # STORAGE_API_URL: str = get_secret("STORAGE_API_URL", "http://localhost:5307/api/v1/storage")

    REDIS_HOST: str = get_secret("REDIS_HOST", "localhost")  # redis_develop
    REDIS_PORT: int = get_secret("REDIS_PORT", 6379)
    REDIS_DB: int = get_secret("REDIS_DB", 2)
    REDIS_CHARSET: str = get_secret("REDIS_CHARSET", "UTF-8")
    REDIS_DECODE_RESPONSES: bool = get_secret("REDIS_DECODE_RESPONSES", True)

    SMS_URL: Optional[str] = get_secret("SMS_USER", "https://smsvas.com/bulk/public/index.php/api/v1/sendsms")
    SMS_USER: Optional[str] = get_secret("SMS_USER", "support@kevmax.com")
    SMS_PASSWORD: Optional[str] = get_secret("SMS_PASSWORD", "kevmax2021")
    SMS_SENDER: Optional[str] = get_secret("SMS_SENDER", "KevMax")

    LOCAL: bool = os.getenv("LOCAL", True)

    class Config:
        case_sensitive = True

    print(f"the db url:{SQLALCHEMY_DATABASE_URL}")


Config = ConfigClass()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SESSION_TOKEN_EXPIRE_SECONDS: int
    DEBUG: bool = False
    TOKEN_TYPE: str
    ADMIN_SECRET_KEY: str
    APP_DIR: str
    UPLOADS_DIR: str

    class Config:
        env_file = ".env"


settings = Settings()

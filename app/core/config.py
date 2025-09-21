from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB:str
    DB_HOST: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SESSION_TOKEN_EXPIRE_SECONDS: int
    DEBUG: bool = False
    TOKEN_TYPE: str = "bearer"
    
    class Config:
        env_file = ".env"

settings = Settings()
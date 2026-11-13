from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_host: str
    database_name: str
    database_user: str
    database_password: str
    database_drivername: str
    database_port: int

    model_config = SettingsConfigDict(env_file=".env")


config = Config()

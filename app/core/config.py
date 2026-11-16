from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_host: str
    database_name: str
    database_user: str
    database_password: str
    database_drivername: str
    database_port: int

    jwt_access_token_expiration_minute: int
    jwt_refresh_token_expiration_minute: int
    jwt_hashing_algorithm: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()

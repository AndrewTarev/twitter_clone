from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


class ApiV1Prefix(BaseModel):
    tweets: str = "/api/tweets"
    users: str = "/api/users"
    medias: str = "/api/medias"


class DatabaseConfig(BaseSettings):

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # авто наминг для ключей БД алембик
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class TestingConfig(BaseModel):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5430
    POSTGRES_NAME: str = "test_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class Settings(BaseModel):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
    )
    api: ApiV1Prefix = ApiV1Prefix()
    db: DatabaseConfig = DatabaseConfig()
    test_db: TestingConfig = TestingConfig()
    logging: str = "INFO"


settings = Settings()


if __name__ == "__main__":
    print(settings.api.likes)

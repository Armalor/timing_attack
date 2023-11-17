from pydantic import Field, BaseSettings, Extra, PostgresDsn
from typing import Optional

from logging import getLogger
from pathlib import Path

# Уверенно полагаем, что config.py всегда лежит в корневом каталоге нашего кода:
__root__ = Path(__file__).parent  # На всякий случай: первый «parent» от __file__ — отдает текущий каталог.
env_file = __root__ / ".env"

logger = getLogger("uvicorn.default")


class FastAPIMixin:
    """ Миксин строки подключения к FastAPI """

    @property
    def dsn(self):
        """ DSN-строка подключения """
        dsn = f'http://{self.host}:{self.port}'
        return dsn


class Settings(BaseSettings):
    class Config:
        """ Параметры """
        env_file: Path = env_file
        env_file_encoding: str = "utf-8"
        extra = Extra.ignore
        case_sensitive = False


class FastAPISettings(FastAPIMixin, Settings):
    """ Параметры подключения к сервису FastAPI """

    host: str = Field(env="FASTAPI_HOST")
    port: int = Field(env="FASTAPI_PORT")
    workers: int = Field(env="FASTAPI_WORKERS")

    login: str = Field(env="FASTAPI_LOGIN")
    password: str = Field(env="FASTAPI_PASSWORD")


class ServiceSettings(Settings):
    fastapi: FastAPISettings = FastAPISettings()

    version: str = Field(env="VERSION")


class Config:
    """ Сервис получает актуальную конфигурацию из переменных окружения """

    config: ServiceSettings = None

    @classmethod
    def get_instance(cls) -> Optional[ServiceSettings]:
        """ Возвращает валидный актуальный конфиг сервиса """

        if not cls.config:

            try:
                cls.config = ServiceSettings()
            except Exception as exc:
                logger.error(exc)

        return cls.config

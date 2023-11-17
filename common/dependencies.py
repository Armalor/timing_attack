from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
import secrets
import asyncio
import itertools

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(str(__root__))

from config import Config
# ~Локальный импорт

security = HTTPBasic()
config = Config.get_instance()


class Dependencies:

    LOGIN = config.fastapi.login
    PASSWORD = config.fastapi.password

    @staticmethod
    async def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = Dependencies.LOGIN.encode("utf8")
        #
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )

        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = Dependencies.PASSWORD.encode("utf8")
        #
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

        if not (is_correct_username and is_correct_password):
            await asyncio.sleep(5)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    @staticmethod
    async def encode(s: str):
        """ Эта функция имитирует нагрузочную операцию побуквенного кодирования пароля.
        Здесь специально вводится задержка для облегчения расчета результатов timing attack.
        Если вы сможете обойтись без нее, это будет БОЛЬШИМ плюсом.
        """

        await asyncio.sleep(0.005)

        return s.encode('utf8') if s else None

    @staticmethod
    async def basic_auth_insecure(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

        current_username = credentials.username
        correct_username = Dependencies.LOGIN

        is_correct_username = True

        for curent_letter, correct_letter in itertools.zip_longest(current_username, correct_username, fillvalue=None):

            curent_letter_byte = await Dependencies.encode(curent_letter)
            correct_letter_byte = await Dependencies.encode(correct_letter)

            if curent_letter_byte != correct_letter_byte:
                is_correct_username = False
                break

        # current_password_bytes = credentials.password.encode("utf8")
        # correct_password_bytes = f"{Dependencies.PASS}".encode("utf8")
        #
        # is_correct_password = current_password_bytes == correct_password_bytes

        # if not (is_correct_username and is_correct_password):
        if not is_correct_username:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Incorrect username or password: {credentials.username}, {credentials.password}",
                headers={"WWW-Authenticate": "Basic"},
            )
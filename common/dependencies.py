from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
import secrets
import asyncio

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(str(__root__))
# ~Локальный импорт

security = HTTPBasic()


class Dependencies:

    LOGIN = 'user'
    PASS = 'pwd'

    @staticmethod
    async def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = f"{Dependencies.LOGIN}".encode("utf8")
        #
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )

        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = f"{Dependencies.PASS}".encode("utf8")
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
    async def basic_auth_insecure(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = f"{Dependencies.LOGIN}".encode("utf8")

        is_correct_username = current_username_bytes == correct_username_bytes

        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = f"{Dependencies.PASS}".encode("utf8")

        is_correct_password = current_password_bytes == correct_password_bytes

        if not (is_correct_username and is_correct_password):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Incorrect username or password: {credentials.username}, {credentials.password}",
                headers={"WWW-Authenticate": "Basic"},
            )
from fastapi import FastAPI, Depends
import uvicorn

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(str(__root__))

from common import Dependencies
from config import Config
# ~Локальный импорт

app = FastAPI(dependencies=[Depends(Dependencies.basic_auth_insecure)])
config = Config.get_instance()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.fastapi.host, port=config.fastapi.port,  workers=config.fastapi.workers)

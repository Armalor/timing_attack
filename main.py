from fastapi import FastAPI, Depends

# Локальный импорт:
from common import Dependencies
# ~Локальный импорт

app = FastAPI(dependencies=[Depends(Dependencies.basic_auth_insecure)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

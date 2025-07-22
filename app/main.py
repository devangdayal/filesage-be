# app/main.py
from app.api.api import router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(router)

def start():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()

from fastapi import FastAPI
from app.api.api import router as api_router

app = FastAPI(title="FileSage Backend")

app.include_router(api_router)

def start():
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

from lib.logging import setup_logging
from lib.config import get_config
from similarity.entrypoints import router as restapi_router
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(restapi_router)


def start_http_server():
    uvicorn.run(
        "main:app",
        **get_config("uvicorn")

    )

if __name__ == "__main__":
    setup_logging()
    start_http_server()

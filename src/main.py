# from lib.logging import setup_logging
from lib.config import get_config
from similarity.entrypoints import router as restapi_router
from similarity.entrypoints.error import init_error_handler
from similarity.entrypoints.restapi import knowledge_base
from similarity.container import Container
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(restapi_router)
init_error_handler(app, 'contact@neonkid.xyz')

# Insert Container (IoC)
container = Container()
container.wire(modules=[knowledge_base])


def start_http_server():
    uvicorn.run(
        "main:app",
        **get_config("uvicorn")

    )

if __name__ == "__main__":
    # setup_logging()

    start_http_server()

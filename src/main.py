# from lib.logging import setup_logging
from lib.config import get_config
from similarity.entrypoints import knowledge_base_router
from similarity.entrypoints import document_router
from similarity.entrypoints.error import init_error_handler
from similarity.entrypoints import restapi
from similarity.container import Container
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(knowledge_base_router)
app.include_router(document_router)
init_error_handler(app, get_config("email"))

# Insert Container (IoC)
container = Container()
container.wire(modules=[restapi.knowledge_base, restapi.document])


def start_http_server():
    uvicorn.run("main:app", **get_config("uvicorn"))


if __name__ == "__main__":
    # setup_logging()

    start_http_server()

from lib.config import get_config

from similarity import entrypoints as router
from similarity.entrypoints.error import init_error_handler

from fastapi import FastAPI
import uvicorn
import asyncio


app = FastAPI()
app.include_router(router.knowledge_base_router)
app.include_router(router.document_router)
app.include_router(router.similarity_router, prefix='/graphql', tags=['GraphQL'], include_in_schema=False)
init_error_handler(app, get_config("email"))

# Insert Container (IoC)


def start_http_server():
    from similarity.container import APIContainer
    container = APIContainer()
    app.container = container
    container.wire(modules=[router.restapi.knowledge_base, router.restapi.document, router.graphql.query])
    uvicorn.run("main:app", **get_config("uvicorn"))

def start_consumer():
    from similarity.entrypoints import redis_consumer
    container = redis_consumer.MQContainer()
    container.wire(modules=[redis_consumer])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(redis_consumer.main())

if __name__ == "__main__":
    # setup_logging()
    loop = asyncio.get_event_loop()
    if get_config("app_env") == "consumer":
        start_consumer()
    else:
        start_http_server()

from lib.config import get_config

from similarity import entrypoints as router
from similarity.entrypoints.error import init_error_handler

from similarity.container import Container
from fastapi import FastAPI
import uvicorn
import asyncio


app = FastAPI()
app.include_router(router.knowledge_base_router)
app.include_router(router.document_router)
app.include_router(router.similarity_router, prefix='/graphql', tags=['GraphQL'], include_in_schema=False)
init_error_handler(app, get_config("email"))

# Insert Container (IoC)
container = Container()
container.wire(modules=[router.restapi.knowledge_base, router.restapi.document, router.redis_router, router.graphql.query])

app.container = container
db = container.db()

def start_http_server():
    uvicorn.run("main:app", **get_config("uvicorn"))

if __name__ == "__main__":
    # setup_logging()
    loop = asyncio.get_event_loop()
    if get_config("app_env") == "consumer":
        loop.run_until_complete(router.redis_consumer.main())
    else:
        start_http_server()

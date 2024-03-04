# from lib.logging import setup_logging
from lib.config import get_config
from similarity.entrypoints import knowledge_base_router
from similarity.entrypoints import document_router
from similarity.entrypoints import redis_consumer
from similarity.entrypoints.error import init_error_handler
from similarity.entrypoints import restapi
from similarity.container import Container
from fastapi import FastAPI
import uvicorn
import asyncio


app = FastAPI()
app.include_router(knowledge_base_router)
app.include_router(document_router)
init_error_handler(app, get_config("email"))

# Insert Container (IoC)
container = Container()
container.wire(modules=[restapi.knowledge_base, restapi.document, redis_consumer])

app.container = container


def start_http_server():
    uvicorn.run("main:app", **get_config("uvicorn"))

async def main():
    print("Start Preload")
    await container.db().preload()
    print("End Preload")

if __name__ == "__main__":
    # setup_logging()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    if get_config("app_env") == "consumer":
        loop.run_until_complete(redis_consumer.main())
    else:
        start_http_server()

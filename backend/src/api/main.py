from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.messages.handlers import router as message_router
from src.infra.message_brokers.lifespan import (
    close_message_broker,
    init_message_broker,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    yield
    await close_message_broker()


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='A simple kafka + ddd example',
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(message_router)
    return app

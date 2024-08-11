from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler
from punq import Container

from src.api.v1.routers import router_v1
from src.infra.di.containers import init_container
from src.infra.message_brokers.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)

    job = await scheduler.spawn(consume_in_background())

    yield
    await close_message_broker()
    await job.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='A simple kafka + ddd example',
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(router_v1, prefix='/api')
    return app

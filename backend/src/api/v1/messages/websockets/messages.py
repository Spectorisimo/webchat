from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
)

from punq import Container
from starlette.websockets import WebSocketDisconnect

from src.application.exceptions.messages import ChatNotFoundException
from src.application.mediator.base import Mediator
from src.application.queries.messages import GetChatDetailQuery
from src.infra.di.containers import init_container
from src.infra.websocket.managers import BaseConnectionManager


router = APIRouter(
    prefix='/chats',
    tags=['Chats'],
)


@router.websocket('/{chat_oid}/')
async def websocket_endpoint(
        chat_oid: str,
        websocket: WebSocket,
        container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ChatNotFoundException as error:
        await websocket.accept()
        await websocket.send_json(data={'error': error.message})
        await websocket.close()
        return

    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    await websocket.send_text("You are now connected!")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)

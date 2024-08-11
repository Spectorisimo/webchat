from fastapi import APIRouter

from src.api.v1.messages.handlers import router as message_router
from src.api.v1.messages.websockets.messages import router as message_ws_router


router_v1 = APIRouter(
    prefix='/v1',
)
router_v1.include_router(message_router)
router_v1.include_router(message_ws_router)

from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi import status

from src.api.schemas import ErrorSchema
from src.api.v1.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from src.application.commands.messages import CreateChatCommand
from src.infra.di.containers import init_container
from src.application.mediator import Mediator
from src.domain.exceptions.base import ApplicationException

router = APIRouter(
    prefix='/chat',
    tags=['Chat'],
)


@router.post(
    '/',
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container=Depends(init_container)
) -> CreateChatResponseSchema:
    """ Create new chat """
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat=chat)

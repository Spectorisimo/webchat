from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from src.api.schemas import ErrorSchema
from src.api.v1.messages.filters import MessagesFilter
from src.api.v1.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    MessageDetailSchema,
    MessagesResponseSchema,
)
from src.application.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from src.application.mediator.base import Mediator
from src.application.mediator.command import CommandMediator
from src.application.mediator.query import QueryMediator
from src.application.queries.messages import (
    GetChatDetailQuery,
    GetMessagesQuery,
)
from src.domain.exceptions.base import ApplicationException
from src.infra.di.containers import init_container

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
    },
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Create new chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat=chat)


@router.post(
    '/{chat_oid}/messages',
    response_model=CreateMessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_message_handler(
        chat_oid: str,
        schema: CreateMessageRequestSchema,
        container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Create message into chat."""
    mediator: CommandMediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateMessageResponseSchema.from_entity(message=message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_chat_with_messages_handler(
        chat_oid: str,
        container: Container = Depends(init_container),
) -> ChatDetailSchema:
    """Get chat info and it messages."""
    mediator: QueryMediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return ChatDetailSchema.from_entity(chat)


@router.get(
    '/{chat_oid}/messages/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': MessagesResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_chat_messages_handler(
        chat_oid: str,
        filters: MessagesFilter = Depends(),
        container: Container = Depends(init_container),
) -> MessagesResponseSchema:
    """Get chat info and it messages."""
    mediator: QueryMediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(
                chat_oid=chat_oid,
                filters=filters.to_infra(),
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return MessagesResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )

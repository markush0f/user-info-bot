from fastapi import APIRouter, Depends
from uuid import UUID
from sqlmodel import Session

from app.core.db import get_session
from app.domains.chats.schemas.send_message_request import SendMessageRequest
from app.domains.chats.service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/create/{user_id}")
def create_chat(
    user_id: UUID,
    session: Session = Depends(get_session),
):
    # Added: inject session into ChatService
    service = ChatService(session)
    chat = service.create_chat(user_id)
    return {"chat_id": chat.id}


@router.post("/send/{chat_id}/{user_id}")
async def send_message(
    chat_id: UUID,
    user_id: UUID,
    body: SendMessageRequest,
    session: Session = Depends(get_session),
):
    # Added: inject session into ChatService
    service = ChatService(session)
    reply = await service.send_message(chat_id, user_id, body.message)
    return {"reply": reply}


@router.get("/{chat_id}")
def get_chat(
    chat_id: UUID,
    session: Session = Depends(get_session),
):
    service = ChatService(session)
    return service.get_chat(chat_id)


@router.get("/user/{user_id}")
def get_chats_by_user(
    user_id: UUID,
    session: Session = Depends(get_session),
):
    service = ChatService(session)
    return service.get_chats_by_user(user_id)


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: UUID,
    session: Session = Depends(get_session),
):
    service = ChatService(session)
    service.delete_chat(chat_id)
    return {"deleted": True}

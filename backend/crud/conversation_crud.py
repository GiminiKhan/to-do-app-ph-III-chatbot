from sqlmodel import Session, select
import sys
import os
# Add backend directory to path to allow imports from models
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from models.conversation_model import Conversation

def create_conversation(session: Session, conversation: Conversation):
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation

def get_conversation(session: Session, thread_id: str):
    return session.exec(select(Conversation).where(Conversation.thread_id == thread_id)).first()
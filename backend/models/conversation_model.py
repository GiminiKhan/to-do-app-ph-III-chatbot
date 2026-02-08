from sqlmodel import SQLModel, Field 
from typing import Optional 
from datetime import datetime 
 
class Conversation(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    thread_id: str = Field(index=True) 
    user_id: str

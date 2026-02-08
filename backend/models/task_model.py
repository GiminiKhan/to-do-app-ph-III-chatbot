from sqlmodel import SQLModel, Field 
from typing import Optional 
from datetime import datetime 
 
class Task(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    title: str 
    status: str = Field(default="pending") 
    priority: str = Field(default="medium")

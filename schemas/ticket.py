from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    title:str
    description:str
    user_id:int
    
class TicketUpdate(BaseModel):
    status: Optional[str] = None
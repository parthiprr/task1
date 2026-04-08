from pydantic import BaseModel

class TicketCreate(BaseModel):
    title:str
    description:str
    user_id:int
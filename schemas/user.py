from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    password:str
    role: str = "user"
    
class UserLogin(BaseModel):
    name:str
    password:str


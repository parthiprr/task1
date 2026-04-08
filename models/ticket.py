from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Ticket(Base):
    __tablename__="tickets"
    
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String)
    status=Column(String,default="OPEN")
    
    user_id=Column(Integer,ForeignKey("users.id"))
    
    user=relationship("User",back_populates="tickets")
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.ticket import Ticket
from schemas.ticket import TicketCreate


router = APIRouter()

@router.post("/")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        user_id=ticket.user_id
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket
    
    
@router.get("/")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()
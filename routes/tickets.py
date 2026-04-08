from fastapi import APIRouter

router = APIRouter()

tickets = []

# Create ticket
@router.post("/")
async def create_ticket(title: str, description: str, user_id: int):
    ticket = {
        "id": len(tickets) + 1,
        "title": title,
        "description": description,
        "status": "OPEN",
        "user_id": user_id
    }
    tickets.append(ticket)
    return ticket

# Get all tickets
@router.get("/")
async def get_tickets():
    return tickets
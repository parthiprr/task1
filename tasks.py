def process_ticket(ticket_id: int):
    print(f"Background Task Running: Ticket {ticket_id} processed")
    
from utils.logger import get_logger

logger=get_logger(__name__)

def process_ticket(ticket_id: int):
    logger.info(f"Ticket {ticket_id} processed")
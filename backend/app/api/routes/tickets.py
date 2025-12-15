from fastapi import APIRouter, HTTPException
from app.services.ticket_service import TicketService
from app.models.ticket import TicketCreate

router = APIRouter()

service = TicketService()

@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketCreate):
    saved = service.create_ticket(ticket)
    return {"id": saved["id"], "status": "created"}

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int):
    ticket = service.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

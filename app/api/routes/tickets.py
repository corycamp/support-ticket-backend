from fastapi import APIRouter, HTTPException, Depends
from app.models.ticket import TicketCreate
from app.services.ticket_service import get_ticket_service, TicketService

router = APIRouter()

@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketCreate, service: TicketService = Depends(get_ticket_service)):
    saved = service.create_ticket(ticket)
    return {"id": saved["id"], "status": "created"}

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int, service: TicketService = Depends(get_ticket_service)):
    ticket = service.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/")
async def list_tickets(service: TicketService = Depends(get_ticket_service)):
    return service.list_tickets()

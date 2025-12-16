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

@router.put("/{ticket_id}/title", response_model=dict)
async def update_ticket_title(ticket_id: int, new_title: str, service: TicketService = Depends(get_ticket_service)):
    updated = service.update_ticket_title(ticket_id, new_title)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"id": updated["id"], "title": updated["title"]}

@router.put("/{ticket_id}/description", response_model=dict)
async def update_ticket_description(ticket_id: int, new_description: str, service: TicketService = Depends(get_ticket_service)):
    updated = service.update_ticket_description(ticket_id, new_description)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"id": updated["id"], "description": updated["description"]}

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, service: TicketService = Depends(get_ticket_service)):
    deleted = service.delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"id": deleted["id"], "status": "deleted"}
@router.put("/{ticket_id}/status", response_model=dict)
async def update_ticket_status(ticket_id: int, new_status: str, service: TicketService = Depends(get_ticket_service)):
    updated_ticket = service.update_ticket_status(ticket_id, new_status)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"id": updated_ticket["id"], "new_status": updated_ticket["status"]}

@router.put("/{ticket_id}/priority", response_model=dict)
async def update_ticket_priority(ticket_id: int, new_priority: str, service: TicketService = Depends(get_ticket_service)):
    updated_ticket = service.update_ticket_priority(ticket_id, new_priority)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"id": updated_ticket["id"], "new_priority": updated_ticket["priority"]}

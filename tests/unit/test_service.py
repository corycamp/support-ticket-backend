import pytest
from app.services.ticket_service import TicketService
from app.models.ticket import TicketCreate

# def test_create_and_get_ticket():
#     svc = TicketService()
#     t = TicketCreate(title="Test", description="desc")
#     saved = svc.create_ticket(t)
#     assert saved["id"] == 1
#     assert svc.get_ticket(1)["title"] == "Test"

from typing import Dict
from app.models.ticket import TicketCreate

class TicketService:
    def __init__(self):
        self._store: Dict[int, Dict] = {}
        self._next = 1

    def create_ticket(self, ticket: TicketCreate) -> Dict:
        tid = self._next
        self._next += 1
        data = {"id": tid, "title": ticket.title, "description": ticket.description}
        self._store[tid] = data
        return data

    def get_ticket(self, ticket_id: int):
        return self._store.get(ticket_id)

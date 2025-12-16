from typing import Dict, Optional
from app.core.utils import now_iso
from app.models.ticket import TicketCreate
from app.services.comment_service import CommentService
from threading import Lock

class InMemoryRepo:
    def __init__(self):
        self._store: Dict[int, Dict] = {}
        self._next = 1
        self._lock = Lock()

    def save(self, data: Dict) -> Dict:
        with self._lock:
            tid = self._next
            self._next += 1
            data = dict(data, id=tid)
            self._store[tid] = data
            return data

    def get(self, tid: int) -> Optional[Dict]:
        return self._store.get(tid)

    def list(self):
        return list(self._store.values())

class TicketService:
    def __init__(self, repo: Optional[InMemoryRepo] = None, comment_repo: Optional[InMemoryRepo] = None):
        self.repo = repo or InMemoryRepo()
        self.comment_repo = comment_repo

    def create_ticket(self, ticket: TicketCreate) -> Dict:
        data = {"title": ticket.title, "description": ticket.description, "created_at": now_iso(), "status": ticket.status, "priority": ticket.priority}
        return self.repo.save(data)

    def get_ticket(self, ticket_id: int):
        comments = ""
        ticket = self.repo.get(ticket_id)
        return {**ticket, "comments": comments} if ticket else {}
    
    def list_tickets(self):
        tickets = []    
        for ticket in self.repo.list():
            comments = self.comment_repo.list_for_ticket(ticket.get("id")) if self.comment_repo else []
            tickets.append({**ticket, "comments": comments})
        return tickets

# FastAPI dependency provider
_ticket_service_singleton: Optional[TicketService] = None

def get_ticket_service() -> TicketService:
    return _ticket_service_singleton

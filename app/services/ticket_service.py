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
    def __init__(self, repo: Optional[InMemoryRepo] = None, comment_service: Optional[CommentService] = None):
        self.repo = repo or InMemoryRepo()
        # Comment service provides `list_comments_for_ticket`; may be a DB-backed service or in-memory
        self.comment_service = comment_service

    def create_ticket(self, ticket: TicketCreate) -> Dict:
        data = {"title": ticket.title, "description": ticket.description, "created_at": now_iso(), "status": ticket.status, "priority": ticket.priority}
        return self.repo.save(data)

    def get_ticket(self, ticket_id: int):
        comments = self.comment_service.list_comments_for_ticket(ticket_id) if self.comment_service else []
        ticket = self.repo.get(ticket_id)
        return {**ticket, "comments": comments} if ticket else {}
    
    def list_tickets(self):
        tickets = []    
        for ticket in self.repo.list():
            comments = self.comment_service.list_comments_for_ticket(ticket.get("id")) if self.comment_service else []
            tickets.append({**ticket, "comments": comments})
        return tickets

# FastAPI dependency provider
_ticket_service_singleton: Optional[TicketService] = None

def get_ticket_service() -> TicketService:
    global _ticket_service_singleton
    if _ticket_service_singleton is None:
        # Lazily create an in-memory service if the app lifecycle didn't initialize a singleton
        _ticket_service_singleton = TicketService()
    return _ticket_service_singleton

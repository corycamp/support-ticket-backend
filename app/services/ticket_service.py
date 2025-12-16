"""Service layer for ticket operations.

This module exposes a `TicketService` that handles ticket creation,
retrieval and listing. A lightweight `InMemoryRepo` is included for
local testing and demos; production code should pass a DB-backed repo
implementing the same `save/get/list` methods.

`TicketService` can be initialized with an optional `comment_service`.
When provided, comments are attached to ticket responses using the
`CommentService.list_comments_for_ticket` API — this keeps concerns
separated and avoids direct access to another service's internals.
"""

from typing import Dict, Optional
from app.core.utils import now_iso
from app.models.ticket import TicketCreate
from app.services.comment_service import CommentService
from threading import Lock

class InMemoryRepo:
    """A simple thread-safe in-memory repository used for tests.

    This class provides `save`, `get`, and `list` methods that mirror the
    interface expected by the `TicketService`. It uses a `threading.Lock`
    to prevent race conditions when running under multiple threads in
    the same process (but does not address multi-process concurrency).
    """
    def __init__(self):
        self._store: Dict[int, Dict] = {}
        self._next = 1
        self._lock = Lock()

    def save(self, data: Dict) -> Dict:
        """Persist `data` in memory and return it with an `id` assigned."""
        with self._lock:
            tid = self._next
            self._next += 1
            data = dict(data, id=tid)
            self._store[tid] = data
            return data

    def get(self, tid: int) -> Optional[Dict]:
        """Return stored item by id or None."""
        return self._store.get(tid)

    def list(self):
        """Return a list of all stored items."""
        return list(self._store.values())

    def update_title_description(self, ticket_id: int, new_title: Optional[str], new_description: Optional[str]) -> Optional[Dict]:
        """Update title and/or description for an in-memory ticket."""
        with self._lock:
            ticket = self._store.get(ticket_id)
            if not ticket:
                return None
            if new_title is not None:
                ticket["title"] = new_title
            if new_description is not None:
                ticket["description"] = new_description
            self._store[ticket_id] = ticket
            return ticket

    def update_status(self, ticket_id: int, new_status: str) -> Optional[Dict]:
        """Update the status field of an in-memory ticket."""
        with self._lock:
            ticket = self._store.get(ticket_id)
            if not ticket:
                return None
            ticket["status"] = new_status
            self._store[ticket_id] = ticket
            return ticket

    def update_priority(self, ticket_id: int, new_priority: str) -> Optional[Dict]:
        """Update the priority field of an in-memory ticket."""
        with self._lock:
            ticket = self._store.get(ticket_id)
            if not ticket:
                return None
            ticket["priority"] = new_priority
            self._store[ticket_id] = ticket
            return ticket

    def delete(self, ticket_id: int) -> Optional[Dict]:
        """Delete a ticket from the in-memory store and return it, or None."""
        with self._lock:
            return self._store.pop(ticket_id, None)

class TicketService:
    """Service for managing tickets.

    Responsibilities:
    - create_ticket: validate and persist tickets (delegates to repo.save)
    - get_ticket: return a ticket with its associated comments (using
      `comment_service.list_comments_for_ticket` when available)
    - update_ticket_status / update_ticket_priority: convenience methods
      that delegate to the repository if the repo provides the operations
    - list_tickets: list tickets and attach comments for each ticket

    The `repo` should implement `save`, `get`, and `list`. The class
    intentionally delegates comment retrieval to a provided
    `comment_service` to avoid accessing another service's internals.
    """
    def __init__(self, repo: Optional[InMemoryRepo] = None, comment_service: Optional[CommentService] = None):
        self.repo = repo or InMemoryRepo()
        # Comment service provides `list_comments_for_ticket`; may be a DB-backed service or in-memory
        self.comment_service = comment_service

    def create_ticket(self, ticket: TicketCreate) -> Dict:
        """Create and persist a ticket, returning its representation."""
        data = {"title": ticket.title, "description": ticket.description, "created_at": now_iso(), "status": ticket.status, "priority": ticket.priority}
        return self.repo.save(data)

    def get_ticket(self, ticket_id: int):
        """Return a ticket dict including `comments` list (empty if none)."""
        comments = self.comment_service.list_comments_for_ticket(ticket_id) if self.comment_service else []
        ticket = self.repo.get(ticket_id)
        return {**ticket, "comments": comments} if ticket else {}
    
    def update_ticket_status(self, ticket_id: int, new_status: str):
        """Update ticket status via repository; return updated record or None."""
        return self.repo.update_status(ticket_id, new_status)
    
    def update_ticket_priority(self, ticket_id: int, new_priority: str):
        """Update ticket priority via repository; return updated record or None."""
        return self.repo.update_priority(ticket_id, new_priority)

    def update_ticket_title(self, ticket_id: int, new_title: str):
        """Update ticket title and return updated record or None."""
        return self.repo.update_title_description(ticket_id, new_title, None)

    def update_ticket_description(self, ticket_id: int, new_description: str):
        """Update ticket description and return updated record or None."""
        return self.repo.update_title_description(ticket_id, None, new_description)

    def delete_ticket(self, ticket_id: int):
        """Delete a ticket and return the deleted record or None."""
        return self.repo.delete(ticket_id)
    
    def list_tickets(self):
        """List tickets and attach associated comments for each."""
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
        _ticket_service_singleton = TicketService()
    return _ticket_service_singleton

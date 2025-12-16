"""Comment service layer.

Provides a consistent API for creating, retrieving and listing comments
and supports either an in-memory store (default) or a repo-backed
implementation (e.g., a DB repo). Use the repo parameter to delegate
persistence to a different storage layer.
"""

from typing import Dict, Optional
from app.core.utils import now_iso
from app.models.comment import CommentCreate


class CommentService:
    """Manage comments for tickets.

    This service exposes methods to create, retrieve, update and list
    comments. When initialized with a `repo` argument it delegates
    persistence operations to the repo; otherwise it falls back to an
    in-memory dict (useful for tests and demos).

    Thread/process safety: the in-memory store is not safe for multi-
    process deployments; prefer a DB-backed repo in production.
    """
    def __init__(self, repo: Optional[object] = None):
        # repo should implement save/get/list_for_ticket/list_all
        self.repo = repo
        if self.repo is None:
            self._store: Dict[int, Dict] = {}
            self._next = 1 
    
    async def create_comment(self, comment: CommentCreate) -> Dict:
        data = {
            "ticket_id": comment.ticket_id,
            "user_email": comment.user_email,
            "content": comment.content,
            "created_at": now_iso()
        }
        if self.repo:
            return self.repo.save(data)
        cid = self._next
        self._next += 1
        data = {"id": cid, **data}
        self._store[cid] = data
        return data
    
    def get_comment(self, comment_id: int):
        return self.repo.get(comment_id) if self.repo else self._store.get(comment_id)
    
    def list_comments(self):
        return self.repo.list_all() if self.repo else list(self._store.values())
    
    def update_comment_content(self, comment_id: int, new_content: str):
        if self.repo:
            return self.repo.update_content(comment_id, new_content)
        comment = self._store.get(comment_id)
        if not comment:
            return None
        comment["content"] = new_content
        return comment

    def delete_comment(self, comment_id: int):
        """Delete a comment and return deleted record or None."""
        if self.repo:
            return self.repo.delete(comment_id)
        comment = self._store.pop(comment_id, None)
        return comment

    def list_comments_for_ticket(self, ticket_id: int):
        return self.repo.list_for_ticket(ticket_id) if self.repo else [c for c in self._store.values() if c["ticket_id"] == ticket_id]
    
    
# FastAPI dependency provider
_comment_service_singleton: Optional[CommentService] = None
def get_comment_service() -> CommentService:
    global _comment_service_singleton
    if _comment_service_singleton is None:
        _comment_service_singleton = CommentService()
    return _comment_service_singleton
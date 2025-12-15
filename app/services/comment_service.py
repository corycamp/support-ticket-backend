from typing import Dict, Optional
from app.core.utils import now_iso
from app.models.comment import CommentCreate
from app.services.user_service import UserService


class CommentService:
    def __init__(self, repo: Optional[object] = None):
        # repo should implement save/get/list_for_ticket/list_all
        self.repo = repo
        if self.repo is None:
            self._store: Dict[int, Dict] = {}
            self._next = 1 
    
    async def create_comment(self, comment: CommentCreate) -> Dict:
        data = {
            "ticket_id": comment.ticket_id,
            "user_id": comment.user_id,
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

    def list_comments_for_ticket(self, ticket_id: int):
        return self.repo.list_for_ticket(ticket_id) if self.repo else [c for c in self._store.values() if c["ticket_id"] == ticket_id]
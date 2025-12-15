from typing import Dict, Optional
from app.models.user import UserCreate


class UserService:
    def __init__(self, repo: Optional[object] = None):
        # repo should implement save/get/get_by_email/list
        self.repo = repo
        if self.repo is None:
            self._store: Dict[str, Dict] = {}

    def create_user(self, user: UserCreate) -> Dict:
        data = {"email": user.email.lower(), "role": user.role}
        if self.repo:
            return self.repo.save(data)
        self._store[data["email"]] = data
        return data

    async def get_user(self, user_email: str):
        if self.repo:
            return self.repo.get_by_email(user_email)
        return self._store.get(user_email)

    async def list_users(self):
        if self.repo:
            return self.repo.list()
        return list(self._store.values())
    
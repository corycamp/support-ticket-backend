"""User service module.

Provides a thin service layer for user management. Supports an in-
memory fallback for tests/demos and a repo-backed mode when a DB repo
is available. Public API is synchronous except where async is kept for
compatibility with potential async repo implementations.
"""

from typing import Dict, Optional
from app.models.user import UserCreate


class UserService:
    """Manage user creation, lookup and role updates.

    When initialized with a `repo` argument, the service delegates
    storage and retrieval to the repo (which should implement `save`,
    `get_by_email`, `get`, and `list`). When no repo is provided the
    service uses an in-memory dict keyed by email (lowercased).
    """
    def __init__(self, repo: Optional[object] = None):
        self.repo = repo
        if self.repo is None:
            self._store: Dict[str, Dict] = {}

    def create_user(self, user: UserCreate) -> Dict:
        """Create a user and return its stored representation."""
        data = {"email": user.email.lower(), "role": user.role}
        if self.repo:
            return self.repo.save(data)
        self._store[data["email"]] = data
        return data

    async def get_user(self, user_email: str):
        """Return the user for `user_email` (email lookup).

        The method adapts to the configured storage (repo or in-memory).
        """
        if self.repo:
            return self.repo.get_by_email(user_email)
        return self._store.get(user_email)

    async def list_users(self):
        """Return a list of all users."""
        if self.repo:
            return self.repo.list()
        return list(self._store.values())
    
    async def update_user_role(self, user_email: str, new_role: str):
        """Update the role of a user and return the updated record.

        Delegates to the repo when available; otherwise updates the
        in-memory store and returns the modified dict.
        """
        if self.repo:
            return self.repo.update_role(user_email, new_role)
        user = self._store.get(user_email)
        if not user:
            return None
        user["role"] = new_role
        return user

    async def delete_user(self, user_email: str):
        """Delete a user by email and return deleted record or None."""
        if self.repo:
            return self.repo.delete_by_email(user_email)
        return self._store.pop(user_email, None)
    

# FastAPI dependency provider
_user_service_singleton: Optional[UserService] = None
def get_user_service() -> UserService:
    global _user_service_singleton
    if _user_service_singleton is None:
        _user_service_singleton = UserService()
    return _user_service_singleton
import app.db.engine as db
from typing import Callable, Optional, Dict, List
from app.db.models import Ticket, Comment

class TicketRepo:
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    def save(self, data: Dict) -> Dict:
        session = self.session_factory()
        try:
            t = Ticket(**data)
            session.add(t)
            session.commit()
            session.refresh(t)
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get(self, tid: int) -> Optional[Dict]:
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(tid)
            if not t:
                return None
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        except Exception as e:
            raise e
        finally:
            session.close()
    
    def update_status(self, ticket_id: int, new_status: str) -> Optional[Dict]:
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(ticket_id)
            if not t:
                return None
            t.status = new_status
            session.commit()
            session.refresh(t)
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def update_priority(self, ticket_id: int, new_priority: str) -> Optional[Dict]:
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(ticket_id)
            if not t:
                return None
            t.priority = new_priority
            session.commit()
            session.refresh(t)
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_title_description(self, ticket_id: int, new_title: Optional[str], new_description: Optional[str]) -> Optional[Dict]:
        """Update title and/or description for a ticket and return updated dict."""
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(ticket_id)
            if not t:
                return None
            if new_title is not None:
                t.title = new_title
            if new_description is not None:
                t.description = new_description
            session.commit()
            session.refresh(t)
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, ticket_id: int) -> Optional[Dict]:
        """Delete a ticket and return the deleted record dict, or None if missing."""
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(ticket_id)
            if not t:
                return None
            result = {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
            session.delete(t)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def list(self) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Ticket).all()
            return [{"id": r.id, "title": r.title, "description": r.description, "priority": r.priority, "status": r.status, "created_at": r.created_at} for r in rows]
        except Exception:
            try:
                session.rollback()
            except Exception:
                pass
            return []
        finally:
            session.close()

class CommentRepo:
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    def save(self, data: Dict) -> Dict:
        session = self.session_factory()
        try:
            c = Comment(**data)
            session.add(c)
            session.commit()
            session.refresh(c)
            return {"id": c.id, "ticket_id": c.ticket_id, "user_emai": c.user_email, "content": c.content, "created_at": c.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, comment_id: int) -> Optional[Dict]:
        """Delete a comment by id and return the deleted record dict, or None if missing."""
        session = self.session_factory()
        try:
            c = session.query(Comment).get(comment_id)
            if not c:
                return None
            result = {"id": c.id, "ticket_id": c.ticket_id, "user_email": c.user_email, "content": c.content, "created_at": c.created_at}
            session.delete(c)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get(self, cid: int) -> Optional[Dict]:
        session = self.session_factory()
        try:
            c = session.query(Comment).get(cid)
            if not c:
                return None
            return {"id": c.id, "ticket_id": c.ticket_id, "user_email": c.user_email, "content": c.content, "created_at": c.created_at}
        finally:
            session.close()

    def list_for_ticket(self, ticket_id: int) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Comment).filter(Comment.ticket_id == ticket_id).all()
            return [{"id": r.id, "ticket_id": r.ticket_id, "user_email": r.user_email, "content": r.content, "created_at": r.created_at} for r in rows]
        except Exception:
            try:
                session.rollback()
            except Exception:
                pass
            return []
        finally:
            session.close()
            
    def update_content(self, comment_id: int, new_content: str) -> Optional[Dict]:
        session = self.session_factory()
        try:
            c = session.query(Comment).get(comment_id)
            if not c:
                return None
            c.content = new_content
            session.commit()
            session.refresh(c)
            return {"id": c.id, "ticket_id": c.ticket_id, "user_email": c.user_email, "content": c.content, "created_at": c.created_at}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def list_all(self) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Comment).all()
            return [{"id": r.id, "ticket_id": r.ticket_id, "user_email": r.user_email, "content": r.content, "created_at": r.created_at} for r in rows]
        except Exception:
            try:
                session.rollback()
            except Exception:
                pass
            return []
        finally:
            session.close()

class UserRepo:
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    def save(self, data: Dict) -> Dict:
        session = self.session_factory()
        try:
            u = Ticket.__table__  # placeholder to ensure table exists
            from app.db.models import User
            user = User(**data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"id": user.id, "email": user.email, "role": user.role, "created_at": user.created_at}
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error saving user: {e}")
        finally:
            session.close()

    def delete_by_email(self, email: str) -> Optional[Dict]:
        """Delete a user by email and return deleted record dict or None if missing."""
        session = self.session_factory()
        try:
            from app.db.models import User
            u = session.query(User).filter(User.email == email).first()
            if not u:
                return None
            result = {"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at}
            session.delete(u)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error deleting user: {e}")
        finally:
            session.close()

    def get(self, uid: int) -> Optional[Dict]:
        session = self.session_factory()
        try:
            from app.db.models import User
            u = session.query(User).get(uid)
            if not u:
                return None
            return {"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at}
        finally:
            session.close()

    def get_by_email(self, email: str) -> Optional[Dict]:
        session = self.session_factory()
        try:
            from app.db.models import User
            u = session.query(User).filter(User.email == email).first()
            if not u:
                return None
            return {"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at}
        finally:
            session.close()

    def list(self) -> List[Dict]:
        session = self.session_factory()
        try:
            from app.db.models import User
            rows = session.query(User).all()
            return [{"id": r.id, "email": r.email, "role": r.role, "created_at": r.created_at} for r in rows]
        except Exception:
            try:
                session.rollback()
            except Exception:
                pass
            return []
        finally:
            session.close()
            
    def update_role(self, email: str, new_role: str) -> Optional[Dict]:
        session = self.session_factory()
        try:
            from app.db.models import User
            u = session.query(User).filter(User.email == email).first()
            if not u:
                return None
            u.role = new_role
            session.commit()
            session.refresh(u)
            return {"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at}
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error updating user role: {e}")
        finally:
            session.close()

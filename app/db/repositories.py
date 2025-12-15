from typing import Callable, Optional, Dict, List
from app.db.engine import SessionLocal
from app.db.models import Ticket, Comment

class TicketRepo:
    def __init__(self, session_factory: Callable = SessionLocal):
        self.session_factory = session_factory

    def save(self, data: Dict) -> Dict:
        session = self.session_factory()
        try:
            t = Ticket(**data)
            session.add(t)
            session.commit()
            session.refresh(t)
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        finally:
            session.close()

    def get(self, tid: int) -> Optional[Dict]:
        session = self.session_factory()
        try:
            t = session.query(Ticket).get(tid)
            if not t:
                return None
            return {"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "status": t.status, "created_at": t.created_at}
        finally:
            session.close()

    def list(self) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Ticket).all()
            return [{"id": r.id, "title": r.title, "description": r.description, "priority": r.priority, "status": r.status, "created_at": r.created_at} for r in rows]
        finally:
            session.close()

class CommentRepo:
    def __init__(self, session_factory: Callable = SessionLocal):
        self.session_factory = session_factory

    def save(self, data: Dict) -> Dict:
        session = self.session_factory()
        try:
            c = Comment(**data)
            session.add(c)
            session.commit()
            session.refresh(c)
            return {"id": c.id, "ticket_id": c.ticket_id, "user_id": c.user_id, "content": c.content, "created_at": c.created_at}
        finally:
            session.close()

    def get(self, cid: int) -> Optional[Dict]:
        session = self.session_factory()
        try:
            c = session.query(Comment).get(cid)
            if not c:
                return None
            return {"id": c.id, "ticket_id": c.ticket_id, "user_id": c.user_id, "content": c.content, "created_at": c.created_at}
        finally:
            session.close()

    def list_for_ticket(self, ticket_id: int) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Comment).filter(Comment.ticket_id == ticket_id).all()
            return [{"id": r.id, "ticket_id": r.ticket_id, "user_id": r.user_id, "content": r.content, "created_at": r.created_at} for r in rows]
        finally:
            session.close()

    def list_all(self) -> List[Dict]:
        session = self.session_factory()
        try:
            rows = session.query(Comment).all()
            return [{"id": r.id, "ticket_id": r.ticket_id, "user_id": r.user_id, "content": r.content, "created_at": r.created_at} for r in rows]
        finally:
            session.close()

class UserRepo:
    def __init__(self, session_factory: Callable = SessionLocal):
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
        finally:
            session.close()

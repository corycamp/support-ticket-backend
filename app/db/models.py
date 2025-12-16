from app.core.utils import now_iso
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SAEnum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from app.models.ticket import Priority, Status
from app.models.user import Role

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(SAEnum(Priority), default=Priority.MEDIUM)
    status = Column(SAEnum(Status), default=Status.OPEN)
    created_at = Column(DateTime, default=now_iso())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=now_iso())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    role = Column(SAEnum(Role), nullable=False)
    created_at = Column(DateTime, default=now_iso())

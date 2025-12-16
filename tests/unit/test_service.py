import pytest
import asyncio
from app.services.ticket_service import TicketService
from app.services.comment_service import CommentService
from app.services.user_service import UserService
from app.models.ticket import TicketCreate
from app.models.comment import CommentCreate
from app.models.user import UserCreate

def test_create_and_get_ticket():
    svc = TicketService()
    t = TicketCreate(title="Test", description="desc")
    saved = svc.create_ticket(t)
    assert saved["id"] == 1
    assert svc.get_ticket(1)["title"] == "Test"

def test_update_and_delete_ticket():
    svc = TicketService()
    t = TicketCreate(title="Original", description="orig desc")
    saved = svc.create_ticket(t)
    tid = saved["id"]

    updated = svc.update_ticket_title(tid, "New Title")
    assert updated and updated["title"] == "New Title"

    updated = svc.update_ticket_description(tid, "New Description")
    assert updated and updated["description"] == "New Description"

    updated = svc.update_ticket_status(tid, "closed")
    assert updated and updated["status"] == "closed"

    updated = svc.update_ticket_priority(tid, "low")
    assert updated and updated["priority"] == "low"

    deleted = svc.delete_ticket(tid)
    assert deleted and deleted["id"] == tid
    assert svc.get_ticket(tid) == {}

def test_comment_service_flow():
    comment_svc = CommentService()
    # create a ticket and attach comments via TicketService using the comment service
    ticket_svc = TicketService(comment_service=comment_svc)
    t = TicketCreate(title="T", description="D")
    saved_ticket = ticket_svc.create_ticket(t)
    tid = saved_ticket["id"]

    c = CommentCreate(ticket_id=tid, user_email="u@example.com", content="hello")
    created = asyncio.run(comment_svc.create_comment(c))
    cid = created["id"]

    fetched = comment_svc.get_comment(cid)
    assert fetched and fetched["content"] == "hello"

    listed = comment_svc.list_comments_for_ticket(tid)
    assert any(cc["id"] == cid for cc in listed)

    updated = comment_svc.update_comment_content(cid, "goodbye")
    assert updated and updated["content"] == "goodbye"

    deleted = comment_svc.delete_comment(cid)
    assert deleted and deleted["id"] == cid

def test_user_service_flow():
    user_svc = UserService()
    u = UserCreate(email="john@example.com")
    created = user_svc.create_user(u)
    assert created["email"] == "john@example.com"

    fetched = asyncio.run(user_svc.get_user("john@example.com"))
    assert fetched and fetched["email"] == "john@example.com"

    listed = asyncio.run(user_svc.list_users())
    assert any(uu["email"] == "john@example.com" for uu in listed)

    updated = asyncio.run(user_svc.update_user_role("john@example.com", "admin"))
    assert updated and updated["role"] == "admin"

    deleted = asyncio.run(user_svc.delete_user("john@example.com"))
    assert deleted and deleted["email"] == "john@example.com"

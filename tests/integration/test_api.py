from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_ticket_integration():
    # Create a user
    resp = client.post("/users/", json={"email":"alice@example.com"})
    assert resp.status_code == 200

    # Create a ticket
    resp = client.post("/tickets/", json={"title":"IT issue", "description":"Can't login"})
    assert resp.status_code == 200
    body = resp.json()
    tid = body["id"]

    # Create a comment for that ticket
    resp = client.post("/comments/", json={"ticket_id": tid, "user_email": "alice@example.com", "content": "Cannot access my account"})
    assert resp.status_code == 200
    cid = resp.json()["comment_id"]

    # Fetch comment
    resp = client.get(f"/comments/{cid}")
    assert resp.status_code == 200
    assert resp.json()["content"] == "Cannot access my account"

    # Update comment content
    resp = client.put(f"/comments/{cid}/content", params={"new_content": "Updated content"})
    assert resp.status_code == 200
    assert resp.json()["new_content"] == "Updated content"

    # Verify comments list includes the created comment
    resp = client.get(f"/comments/")
    assert resp.status_code == 200
    comments = resp.json()
    assert any(c["id"] == cid for c in comments)

    # Verify ticket fetch still returns ticket
    resp = client.get(f"/tickets/{tid}")
    assert resp.status_code == 200
    ticket = resp.json()
    assert ticket["title"] == "IT issue"

    # Update ticket title and description
    resp = client.put(f"/tickets/{tid}/title", params={"new_title": "Updated Title"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"

    resp = client.put(f"/tickets/{tid}/description", params={"new_description": "Updated Description"})
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated Description"

    # Update status and priority
    resp = client.put(f"/tickets/{tid}/status", params={"new_status": "closed"})
    assert resp.status_code == 200
    assert resp.json()["new_status"] == "closed"

    resp = client.put(f"/tickets/{tid}/priority", params={"new_priority": "low"})
    assert resp.status_code == 200
    assert resp.json()["new_priority"] == "low"

    # Delete comment
    resp = client.delete(f"/comments/{cid}")
    assert resp.status_code == 200

    resp = client.get(f"/comments/{cid}")
    assert resp.status_code == 404

    # Delete ticket
    resp = client.delete(f"/tickets/{tid}")
    assert resp.status_code == 200

    resp = client.get(f"/tickets/{tid}")
    assert resp.status_code == 404

    # Delete user
    resp = client.delete(f"/users/alice@example.com")
    assert resp.status_code == 200

    resp = client.get(f"/users/alice@example.com")
    assert resp.status_code == 404

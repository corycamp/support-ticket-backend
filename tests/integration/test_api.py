from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_ticket_integration():
    resp = client.post("/tickets/", json={"title":"IT issue", "description":"Can't login"})
    assert resp.status_code == 200
    body = resp.json()
    tid = body["id"]
    get = client.get(f"/tickets/{tid}")
    assert get.status_code == 200
    assert get.json()["title"] == "IT issue"

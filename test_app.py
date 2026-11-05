from fastapi.testclient import TestClient
from app import app, client, reports

def test_report_submission(monkeypatch):
    async def send(event): return ["event"]
    monkeypatch.setattr(client, "send", send)
    c=TestClient(app); assert c.post("/reports", json={}).status_code==400
    r=c.post("/reports",json={"topic":"cats"}); assert r.status_code==202
    assert c.get("/reports/"+r.json()["id"]).json()["status"]=="pending"
    assert c.get("/reports/absent").status_code==404

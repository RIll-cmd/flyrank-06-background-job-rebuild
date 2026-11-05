from fastapi.testclient import TestClient
from app import app, client, reports

def test_queue_failure_does_not_leave_a_phantom_pending_report(monkeypatch):
    async def unavailable(event): raise RuntimeError('offline')
    monkeypatch.setattr(client,'send',unavailable)
    before=set(reports)
    response=TestClient(app).post('/reports',json={'topic':'cats'})
    assert response.status_code==503
    assert set(reports)==before

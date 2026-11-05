from fastapi.testclient import TestClient
from app import app

def test_report_requests_require_a_nonempty_string_topic():
    client=TestClient(app)
    for payload in ({}, {'topic':''}, {'topic':'   '}, {'topic':17}, []):
        assert client.post('/reports',json=payload).status_code==400

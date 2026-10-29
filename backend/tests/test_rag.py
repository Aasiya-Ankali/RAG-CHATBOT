# pytest query should come here
# test endpoints should come here
# api/query is endpoint which will come here
# backend/tests/test_rag.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rag():
    response = client.post("/api/query" ,json={"question" :"Which device is best for home automation?"})
    assert response.status_code == 200
    assert "Answer" in response.json()


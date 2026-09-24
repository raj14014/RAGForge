import os
os.environ["DATABASE_URL"]="sqlite:///./test_ragforge.db"
os.environ["LLM_PROVIDER"]="mock"
from fastapi.testclient import TestClient
from app.main import app

def test_health():
    c=TestClient(app)
    assert c.get('/health').json()['status']=='healthy'

import app
import json

def test_token_generation():
    """Test that /token endpoint returns a valid token"""
    client = app.app.test_client()
    res = client.post("/token")
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert isinstance(data["token"], str)

def test_protected_with_valid_token():
    """Test that /protected endpoint accepts valid token in header"""
    client = app.app.test_client()
    token = client.post("/token").get_json()["token"]
    
    res = client.get("/protected", headers={"Token": token})
    assert res.status_code == 200
    data = res.get_json()
    assert data["message"] == "Access granted"
    assert data["user"] == 1

def test_protected_without_token():
    """Test that /protected endpoint rejects requests without token"""
    client = app.app.test_client()
    res = client.get("/protected")
    assert res.status_code == 401
    assert "Missing token" in res.get_json()["error"]

def test_protected_with_invalid_token():
    """Test that /protected endpoint rejects invalid token"""
    client = app.app.test_client()
    res = client.get("/protected", headers={"Token": "invalid_token"})
    assert res.status_code == 401
    assert "Invalid token" in res.get_json()["error"]
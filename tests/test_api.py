from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_shorten_redirect_and_stats():
    r = client.post("/shorten", json={"original_url": "https://example.com"})
    assert r.status_code == 201
    code = r.json()["short_code"]

    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 302

    r = client.get(f"/stats/{code}")
    assert r.status_code == 200
    assert r.json()["total_clicks"] >= 1


def test_unknown_code_returns_404():
    r = client.get("/doesnotexist", follow_redirects=False)
    assert r.status_code == 404
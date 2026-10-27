import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_home_page(client):
    assert client.get("/").status_code == 200


def test_predict_placed(client):
    r = client.post("/predict", json={
        "cgpa": 9.0, "internships": 3, "projects": 5,
        "backlogs": 0, "communication": 9,
    })
    assert r.status_code == 200
    assert r.get_json()["prediction"] == "Placed"


def test_predict_not_placed(client):
    r = client.post("/predict", json={
        "cgpa": 5.2, "internships": 0, "projects": 0,
        "backlogs": 4, "communication": 2,
    })
    assert r.status_code == 200
    assert r.get_json()["prediction"] == "Not Placed"


def test_predict_bad_input(client):
    r = client.post("/predict", json={"cgpa": "abc"})
    assert r.status_code == 400


def test_metrics_endpoint(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"flask_http_request_total" in r.data

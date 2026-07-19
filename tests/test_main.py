import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_and_get_task(client):
    resp = client.post("/tasks", json={"title": "Write CI/CD pipeline"})
    assert resp.status_code == 201
    task = resp.get_json()
    assert task["title"] == "Write CI/CD pipeline"
    assert task["done"] is False

    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.get_json()) >= 1


def test_create_task_without_title(client):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 400


def test_update_task(client):
    resp = client.post("/tasks", json={"title": "Temp task"})
    task_id = resp.get_json()["id"]

    resp = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert resp.status_code == 200
    assert resp.get_json()["done"] is True


def test_update_missing_task(client):
    resp = client.patch("/tasks/9999", json={"done": True})
    assert resp.status_code == 404


def test_delete_task(client):
    resp = client.post("/tasks", json={"title": "To delete"})
    task_id = resp.get_json()["id"]

    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204


def test_delete_missing_task(client):
    resp = client.delete("/tasks/9999")
    assert resp.status_code == 404

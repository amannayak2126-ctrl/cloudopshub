from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "application": "CloudOpsHub",
        "status": "running",
        "version": "1.0.0",
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in [
        "HEALTHY",
        "WARNING",
        "CRITICAL",
    ]

    assert "cpu_usage" in data
    assert "memory_usage" in data
    assert "disk_usage" in data
    assert "uptime" in data


def test_services():
    response = client.get("/services")

    assert response.status_code == 200

    data = response.json()

    assert "services" in data
    assert isinstance(data["services"], dict)


def test_incidents():
    response = client.get("/incidents")

    assert response.status_code == 200

    data = response.json()

    assert "incidents" in data
    assert isinstance(data["incidents"], list)

    for incident in data["incidents"]:
        assert "id" in incident
        assert "service_name" in incident
        assert "status" in incident
        assert "created_at" in incident
        assert "resolved_at" in incident

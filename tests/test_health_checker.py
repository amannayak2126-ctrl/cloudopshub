from monitoring.health_checker import get_health_status


def test_health_status_healthy():
    assert get_health_status(50, 50, 50) == "HEALTHY"


def test_health_status_warning():
    assert get_health_status(75, 50, 50) == "WARNING"
    assert get_health_status(50, 75, 50) == "WARNING"
    assert get_health_status(50, 50, 75) == "WARNING"


def test_health_status_critical():
    assert get_health_status(90, 50, 50) == "CRITICAL"
    assert get_health_status(50, 90, 50) == "CRITICAL"
    assert get_health_status(50, 50, 90) == "CRITICAL"

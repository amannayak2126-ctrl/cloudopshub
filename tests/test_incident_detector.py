from monitoring.incident_detector import IncidentDetector


def test_incident_lifecycle():
    detector = IncidentDetector()

    assert detector.check("nginx", True) is None
    assert detector.check("nginx", False) == "CREATED"
    assert detector.check("nginx", False) is None
    assert detector.check("nginx", True) == "RESOLVED"

import monitoring.database as database


def test_incident_lifecycle(tmp_path, monkeypatch):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_FILE",
        str(test_database),
    )

    database.initialize_database()

    incident_id = database.create_incident("nginx")

    assert incident_id == 1

    incidents = database.get_incidents()

    assert len(incidents) == 1
    assert incidents[0][1] == "nginx"
    assert incidents[0][2] == "OPEN"
    assert incidents[0][4] is None

    resolved = database.resolve_incident("nginx")

    assert resolved is True

    incidents = database.get_incidents()

    assert incidents[0][2] == "RESOLVED"
    assert incidents[0][4] is not None

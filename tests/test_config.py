import importlib


def test_default_config(monkeypatch):
    monkeypatch.delenv(
        "CLOUDOPSHUB_CHECK_INTERVAL",
        raising=False,
    )
    monkeypatch.delenv(
        "CLOUDOPSHUB_LOG_FILE",
        raising=False,
    )
    monkeypatch.delenv(
        "CLOUDOPSHUB_SERVICES",
        raising=False,
    )

    import config

    importlib.reload(config)

    assert config.CHECK_INTERVAL == 10
    assert config.LOG_FILE == "monitoring/cloudopshub.log"
    assert config.MONITORED_SERVICES == ["nginx"]


def test_environment_config(monkeypatch):
    monkeypatch.setenv(
        "CLOUDOPSHUB_CHECK_INTERVAL",
        "5",
    )
    monkeypatch.setenv(
        "CLOUDOPSHUB_LOG_FILE",
        "custom.log",
    )
    monkeypatch.setenv(
        "CLOUDOPSHUB_SERVICES",
        "nginx, ssh, docker",
    )

    import config

    importlib.reload(config)

    assert config.CHECK_INTERVAL == 5
    assert config.LOG_FILE == "custom.log"
    assert config.MONITORED_SERVICES == [
        "nginx",
        "ssh",
        "docker",
    ]

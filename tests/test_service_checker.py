from unittest.mock import patch, Mock

from monitoring.service_checker import check_service


def test_service_is_running():
    mock_result = Mock()
    mock_result.stdout = "active\n"

    with patch(
        "monitoring.service_checker.subprocess.run",
        return_value=mock_result,
    ) as mock_run:

        result = check_service("nginx")

    assert result is True

    mock_run.assert_called_once_with(
        ["systemctl", "is-active", "nginx"],
        capture_output=True,
        text=True,
    )


def test_service_is_down():
    mock_result = Mock()
    mock_result.stdout = "inactive\n"

    with patch(
        "monitoring.service_checker.subprocess.run",
        return_value=mock_result,
    ) as mock_run:

        result = check_service("nginx")

    assert result is False

    mock_run.assert_called_once_with(
        ["systemctl", "is-active", "nginx"],
        capture_output=True,
        text=True,
    )

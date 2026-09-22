import os


def get_check_interval():
    value = os.getenv(
        "CLOUDOPSHUB_CHECK_INTERVAL",
        "10"
    )

    try:
        interval = int(value)
    except ValueError:
        raise ValueError(
            "CLOUDOPSHUB_CHECK_INTERVAL must be an integer."
        )

    if interval <= 0:
        raise ValueError(
            "CLOUDOPSHUB_CHECK_INTERVAL must be greater than 0."
        )

    return interval


def get_log_file():
    value = os.getenv(
        "CLOUDOPSHUB_LOG_FILE",
        "monitoring/cloudopshub.log"
    ).strip()

    if not value:
        raise ValueError(
            "CLOUDOPSHUB_LOG_FILE must not be empty."
        )

    return value


def get_monitored_services():
    services = [
        service.strip()
        for service in os.getenv(
            "CLOUDOPSHUB_SERVICES",
            "nginx"
        ).split(",")
        if service.strip()
    ]

    if not services:
        raise ValueError(
            "CLOUDOPSHUB_SERVICES must contain at least one service."
        )

    return services


CHECK_INTERVAL = get_check_interval()
LOG_FILE = get_log_file()
MONITORED_SERVICES = get_monitored_services()

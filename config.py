import os


CHECK_INTERVAL = int(
    os.getenv("CLOUDOPSHUB_CHECK_INTERVAL", "10")
)


LOG_FILE = os.getenv(
    "CLOUDOPSHUB_LOG_FILE",
    "monitoring/cloudopshub.log"
)


MONITORED_SERVICES = [
    service.strip()
    for service in os.getenv(
        "CLOUDOPSHUB_SERVICES",
        "nginx"
    ).split(",")
    if service.strip()
]

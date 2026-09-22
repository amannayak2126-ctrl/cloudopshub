import time

from monitoring.health_checker import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
    get_health_status,
)
from monitoring.service_checker import check_service
from monitoring.incident_detector import IncidentDetector
from monitoring.database import (
    initialize_database,
    create_incident,
    resolve_incident,
)
from monitoring.logger import get_logger

from config import (
    CHECK_INTERVAL,
    MONITORED_SERVICES,
)


logger = get_logger("monitor")

incident_detectors = {
    service: IncidentDetector()
    for service in MONITORED_SERVICES
}


def perform_health_check():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()

    system_health = get_health_status(
        cpu,
        memory,
        disk,
    )

    service_statuses = []
    service_health = {}

    for service_name in MONITORED_SERVICES:
        service_running = check_service(
            service_name
        )

        service_health[service_name] = service_running

        incident_event = incident_detectors[
            service_name
        ].check(
            service_name,
            service_running,
        )

        service_status = (
            "RUNNING"
            if service_running
            else "DOWN"
        )

        service_statuses.append(
            f"{service_name.upper()}={service_status}"
        )

        if incident_event:
            event_message = (
                f"INCIDENT EVENT: "
                f"{service_name} "
                f"{incident_event}"
            )

            print(event_message)
            logger.info(event_message)

            if incident_event == "CREATED":
                incident_id = create_incident(
                    service_name
                )

                stored_message = (
                    f"INCIDENT STORED: "
                    f"{service_name} "
                    f"ID={incident_id}"
                )

                print(stored_message)
                logger.info(stored_message)

            elif incident_event == "RESOLVED":
                resolved = resolve_incident(
                    service_name
                )

                if resolved:
                    resolved_message = (
                        f"INCIDENT RESOLVED "
                        f"IN DATABASE: "
                        f"{service_name}"
                    )

                    print(resolved_message)
                    logger.info(resolved_message)

                else:
                    warning_message = (
                        f"WARNING: No open "
                        f"{service_name} "
                        f"incident found"
                    )

                    print(warning_message)
                    logger.warning(warning_message)

    overall_status = system_health

    if any(
        not running
        for running in service_health.values()
    ):
        overall_status = "INCIDENT"

    service_status_text = " | ".join(
        service_statuses
    )

    message = (
        f"CPU={cpu:.1f}% | "
        f"MEMORY={memory:.1f}% | "
        f"DISK={disk:.1f}% | "
        f"UPTIME={uptime} | "
        f"{service_status_text} | "
        f"STATUS={overall_status}"
    )

    print(message)
    logger.info(message)


def main():
    initialize_database()

    print("CloudOpsHub Monitoring Service")
    print(
        f"Health check interval: "
        f"{CHECK_INTERVAL} seconds"
    )

    print(
        f"Monitored services: "
        f"{', '.join(MONITORED_SERVICES)}"
    )

    print("Press Ctrl+C to stop.")
    print()

    try:
        while True:
            perform_health_check()
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print(
            "\nCloudOpsHub monitoring stopped."
        )


if __name__ == "__main__":
    main()

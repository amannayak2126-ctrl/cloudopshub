import time
from datetime import datetime

from monitoring.health_checker import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
    get_health_status,
)

from monitoring.service_checker import check_service
from monitoring.incident_detector import IncidentDetector


LOG_FILE = "monitoring/cloudopshub.log"
CHECK_INTERVAL = 10

incident_detector = IncidentDetector()


def write_log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")


def perform_health_check():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()

    system_health = get_health_status(cpu, memory, disk)

    nginx_running = check_service("nginx")

    incident_event = incident_detector.check(
        "nginx",
        nginx_running
    )

    if not nginx_running:
        overall_status = "INCIDENT"
        nginx_status = "DOWN"
    else:
        nginx_status = "RUNNING"
        overall_status = system_health

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"{timestamp} | "
        f"CPU={cpu:.1f}% | "
        f"MEMORY={memory:.1f}% | "
        f"DISK={disk:.1f}% | "
        f"UPTIME={uptime} | "
        f"NGINX={nginx_status} | "
        f"STATUS={overall_status}"
    )

    print(message)
    write_log(message)

    if incident_event:
        event_message = (
            f"{timestamp} | "
            f"INCIDENT EVENT: nginx {incident_event}"
        )

        print(event_message)
        write_log(event_message)


def main():
    print("CloudOpsHub Monitoring Service")
    print(f"Health check interval: {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop.")
    print()

    try:
        while True:
            perform_health_check()
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nCloudOpsHub monitoring stopped.")


if __name__ == "__main__":
    main()

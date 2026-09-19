import time
from datetime import datetime

from monitoring.health_checker import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
    get_health_status,
)


LOG_FILE = "monitoring/cloudopshub.log"
CHECK_INTERVAL = 10


def write_log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")


def perform_health_check():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()

    health = get_health_status(cpu, memory, disk)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"{timestamp} | "
        f"CPU={cpu:.1f}% | "
        f"MEMORY={memory:.1f}% | "
        f"DISK={disk:.1f}% | "
        f"UPTIME={uptime} | "
        f"STATUS={health}"
    )

    print(message)
    write_log(message)


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

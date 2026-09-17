import platform
import shutil
import time

import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    disk = shutil.disk_usage("/")
    return (disk.used / disk.total) * 100


def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()

    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    return f"{days}d {hours}h {minutes}m"


def get_health_status(cpu, memory, disk):
    if cpu >= 90 or memory >= 90 or disk >= 90:
        return "CRITICAL"

    if cpu >= 75 or memory >= 75 or disk >= 75:
        return "WARNING"

    return "HEALTHY"


def main():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()
    health = get_health_status(cpu, memory, disk)

    print("=" * 45)
    print("        CloudOpsHub Health Checker")
    print("=" * 45)

    print(f"Operating System : {platform.system()}")
    print(f"CPU Usage        : {cpu:.1f}%")
    print(f"Memory Usage     : {memory:.1f}%")
    print(f"Disk Usage       : {disk:.1f}%")
    print(f"System Uptime    : {uptime}")
    print(f"Health Status    : {health}")

    print("=" * 45)


if __name__ == "__main__":
    main()
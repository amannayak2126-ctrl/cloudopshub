from fastapi import FastAPI

from config import MONITORED_SERVICES

from monitoring.health_checker import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
    get_health_status,
)

from monitoring.service_checker import check_service

from monitoring.database import (
    initialize_database,
    get_incidents,
)


app = FastAPI(
    title="CloudOpsHub API",
    description="API for CloudOpsHub monitoring and incident data",
    version="1.0.0",
)


initialize_database()


@app.get("/")
def root():
    return {
        "application": "CloudOpsHub",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()

    status = get_health_status(
        cpu,
        memory,
        disk,
    )

    return {
        "status": status,
        "cpu_usage": round(cpu, 1),
        "memory_usage": round(memory, 1),
        "disk_usage": round(disk, 1),
        "uptime": uptime,
    }


@app.get("/services")
def services():
    service_status = {}

    for service_name in MONITORED_SERVICES:
        service_status[service_name] = (
            "RUNNING"
            if check_service(service_name)
            else "DOWN"
        )

    return {
        "services": service_status
    }


@app.get("/incidents")
def incidents():
    incident_rows = get_incidents()

    incident_list = []

    for incident in incident_rows:
        incident_list.append(
            {
                "id": incident[0],
                "service_name": incident[1],
                "status": incident[2],
                "created_at": incident[3],
                "resolved_at": incident[4],
            }
        )

    return {
        "incidents": incident_list
    }

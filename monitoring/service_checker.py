import subprocess


def check_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True,
    )

    status = result.stdout.strip()

    return status == "active"


def main():
    service = "nginx"

    if check_service(service):
        print(f"{service}: RUNNING")
    else:
        print(f"{service}: DOWN")


if __name__ == "__main__":
    main()

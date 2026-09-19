class IncidentDetector:
    def __init__(self):
        self.previous_status = {}

    def check(self, service_name, is_running):
        current_status = "UP" if is_running else "DOWN"
        previous_status = self.previous_status.get(service_name)

        self.previous_status[service_name] = current_status

        if previous_status is None:
            return None

        if previous_status == "UP" and current_status == "DOWN":
            return "CREATED"

        if previous_status == "DOWN" and current_status == "UP":
            return "RESOLVED"

        return None

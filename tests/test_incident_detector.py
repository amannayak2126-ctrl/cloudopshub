from monitoring.incident_detector import IncidentDetector


def main():
    detector = IncidentDetector()

    print("First check:")
    print(detector.check("nginx", True))

    print("Second check - service goes DOWN:")
    print(detector.check("nginx", False))

    print("Third check - service remains DOWN:")
    print(detector.check("nginx", False))

    print("Fourth check - service recovers:")
    print(detector.check("nginx", True))


if __name__ == "__main__":
    main()

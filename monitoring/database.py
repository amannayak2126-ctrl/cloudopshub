import sqlite3


DATABASE_FILE = "monitoring/cloudopshub.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved_at DATETIME
        )
        """
    )

    connection.commit()
    connection.close()


def create_incident(service_name):
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO incidents (
            service_name,
            status
        )
        VALUES (?, ?)
        """,
        (
            service_name,
            "OPEN",
        ),
    )

    connection.commit()

    incident_id = cursor.lastrowid

    connection.close()

    return incident_id


def resolve_incident(service_name):
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE incidents
        SET
            status = 'RESOLVED',
            resolved_at = CURRENT_TIMESTAMP
        WHERE id = (
            SELECT id
            FROM incidents
            WHERE service_name = ?
              AND status = 'OPEN'
            ORDER BY id DESC
            LIMIT 1
        )
        """,
        (service_name,),
    )

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated > 0


def get_incidents():
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            service_name,
            status,
            created_at,
            resolved_at
        FROM incidents
        ORDER BY id DESC
        """
    )

    incidents = cursor.fetchall()

    connection.close()

    return incidents

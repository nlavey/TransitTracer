from fastapi import FastAPI
from src.database.connection import get_connection

app = FastAPI()


@app.get("/health/db")
def database_health_check():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        return {
            "database": "connected",
            "result": result[0]
        }

    finally:
        cursor.close()
        connection.close()


@app.get("/agencies", response_model=list[dict])
def get_agencies():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                agency_id,
                agency_name,
                agency_url,
                agency_timezone
            FROM agency
            ORDER BY agency_name;
        """)

        rows = cursor.fetchall()

        agencies = []

        for row in rows:
            agencies.append({
                "agency_id": row[0],
                "agency_name": row[1],
                "agency_url": row[2],
                "agency_timezone": row[3]
            })

        return agencies

    finally:
        cursor.close()
        connection.close()
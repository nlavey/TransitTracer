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

@app.get("/routes")
def get_routes():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                agency_id,
                route_id,
                route_short_name,
                route_long_name,
                route_desc,
                route_type,
                route_url,
                route_color,
                route_text_color,
                route_sort_order,
                min_headway_minutes,
                eligibility_restricted,
                continuous_pickup,
                continuous_drop_off,
                tts_route_short_name,
                tts_route_long_name
            FROM routes
            ORDER BY route_sort_order, route_short_name;
        """)

        rows = cursor.fetchall()

        routes = []

        for row in rows:
            routes.append({
                "agency_id": row[0],
                "route_id": row[1],
                "route_short_name": row[2],
                "route_long_name": row[3],
                "route_desc": row[4],
                "route_type": row[5],
                "route_url": row[6],
                "route_color": row[7],
                "route_text_color": row[8],
                "route_sort_order": row[9],
                "min_headway_minutes": row[10],
                "eligibility_restricted": row[11],
                "continuous_pickup": row[12],
                "continuous_drop_off": row[13],
                "tts_route_short_name": row[14],
                "tts_route_long_name": row[15]
            })

        return routes

    finally:
        cursor.close()
        connection.close()
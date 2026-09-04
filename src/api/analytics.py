from fastapi import APIRouter
from src.database.connection import get_connection

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/trips-per-route")
def trips_per_route():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                r.route_id,
                r.route_short_name,
                r.route_long_name,
                COUNT(t.trip_id) AS trip_count
            FROM routes r
            JOIN trips t
                ON r.route_id = t.route_id
            GROUP BY
                r.route_id,
                r.route_short_name,
                r.route_long_name
            ORDER BY trip_count DESC;
        """)

        rows = cursor.fetchall()

        return [
            {
                "route_id": row[0],
                "route_short_name": row[1],
                "route_long_name": row[2],
                "trip_count": row[3]
            }
            for row in rows
        ]

    finally:
        connection.close()
from fastapi import APIRouter, HTTPException
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

@router.get("/busiest-stops")
def busiest_stops():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                s.stop_id,
                s.stop_name,
                COUNT(st.trip_id) AS scheduled_events
            FROM stops s
            JOIN stop_times st
                ON s.stop_id = st.stop_id
            GROUP BY
                s.stop_id,
                s.stop_name
            ORDER BY scheduled_events DESC
            LIMIT 10;
        """)

        rows = cursor.fetchall()

        return [
            {
                "stop_id": row[0],
                "stop_name": row[1],
                "scheduled_events": row[2]
            }
            for row in rows
        ]

    finally:
        connection.close()

@router.get("/trips-by-hour")
def trips_by_hour():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            WITH first_stops AS (
                SELECT
                    trip_id,
                    departure_time,
                    ROW_NUMBER() OVER (
                        PARTITION BY trip_id
                        ORDER BY stop_sequence
                    ) AS stop_rank
                FROM stop_times
            )
            SELECT
                CAST(SPLIT_PART(departure_time, ':', 1) AS INTEGER) AS hour,
                COUNT(*) AS trip_count
            FROM first_stops
            WHERE stop_rank = 1
            GROUP BY hour
            ORDER BY hour;
        """)

        rows = cursor.fetchall()

        return [
            {
                "hour": row[0],
                "trip_count": row[1]
            }
            for row in rows
        ]

    finally:
        connection.close()

@router.get("/routes/{route_id}")
def route_statistics(route_id: str):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 FROM routes WHERE route_id = %s",
            (route_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail=f"Route {route_id} not found"
            )

        cursor.execute("""
            WITH route_trips AS (
                SELECT trip_id
                FROM trips
                WHERE route_id = %s
            ),
            trip_stats AS (
                SELECT
                    rt.trip_id,
                    COUNT(st.stop_id) AS stop_count
                FROM route_trips rt
                JOIN stop_times st
                    ON rt.trip_id = st.trip_id
                GROUP BY rt.trip_id
            )

            SELECT
                %s AS route_id,
                (SELECT COUNT(*) FROM route_trips) AS total_trips,
                COUNT(DISTINCT st.stop_id) AS stops_served,
                ROUND(AVG(ts.stop_count), 1) AS average_stops_per_trip
            FROM trip_stats ts
            JOIN stop_times st
                ON ts.trip_id = st.trip_id;
        """, (route_id, route_id))

        row = cursor.fetchone()

        return {
            "route_id": row[0],
            "total_trips": row[1],
            "stops_served": row[2],
            "average_stops_per_trip": float(row[3])
        }

    finally:
        connection.close()
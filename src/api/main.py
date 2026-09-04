from fastapi import FastAPI, Query
from src.database.connection import get_connection
from src.api import analytics

app = FastAPI()

app.include_router(analytics.router)

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

@app.get("/stops")
def get_stops():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                stop_id,
                stop_code,
                stop_name,
                stop_desc,
                stop_lat,
                stop_lon,
                zone_id,
                stop_url,
                location_type,
                parent_station
            FROM stops
            ORDER BY stop_name;
        """)

        rows = cursor.fetchall()

        stops = []

        for row in rows:
            stops.append({
                "stop_id": row[0],
                "stop_code": row[1],
                "stop_name": row[2],
                "stop_desc": row[3],
                "stop_lat": row[4],
                "stop_lon": row[5],
                "zone_id": row[6],
                "stop_url": row[7],
                "location_type": row[8],
                "parent_station": row[9]
            })

        return stops

    finally:
        cursor.close()
        connection.close()

@app.get("/trips")
def get_trips():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                route_id,
                service_id,
                trip_id,
                trip_short_name,
                trip_headsign,
                direction_id,
                block_id,
                shape_id,
                bikes_allowed,
                wheelchair_accessible,
                trip_type,
                drt_max_travel_time,
                drt_avg_travel_time,
                drt_advance_book_min,
                drt_pickup_message,
                drt_drop_off_message,
                continuous_pickup_message,
                continuous_drop_off_message,
                tts_trip_headsign,
                tts_trip_short_name
            FROM trips
            ORDER BY route_id, trip_id;
        """)

        rows = cursor.fetchall()

        trips = []

        for row in rows:
            trips.append({
                "route_id": row[0],
                "service_id": row[1],
                "trip_id": row[2],
                "trip_short_name": row[3],
                "trip_headsign": row[4],
                "direction_id": row[5],
                "block_id": row[6],
                "shape_id": row[7],
                "bikes_allowed": row[8],
                "wheelchair_accessible": row[9],
                "trip_type": row[10],
                "drt_max_travel_time": row[11],
                "drt_avg_travel_time": row[12],
                "drt_advance_book_min": row[13],
                "drt_pickup_message": row[14],
                "drt_drop_off_message": row[15],
                "continuous_pickup_message": row[16],
                "continuous_drop_off_message": row[17],
                "tts_trip_headsign": row[18],
                "tts_trip_short_name": row[19]
            })

        return trips

    finally:
        cursor.close()
        connection.close()

@app.get("/stop-times")
def get_stop_times(
    limit: int = Query(default=100, ge=1, le=1000)
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                trip_id,
                arrival_time,
                departure_time,
                stop_id,
                stop_sequence,
                stop_headsign,
                pickup_type,
                drop_off_type,
                shape_dist_traveled,
                timepoint,
                start_service_area_id,
                end_service_area_id,
                start_service_area_radius,
                end_service_area_radius,
                continuous_pickup,
                continuous_drop_off,
                pickup_booking_rule_id,
                drop_off_booking_rule_id,
                start_pickup_drop_off_window,
                end_pickup_drop_off_window,
                mean_duration_factor,
                mean_duration_offset,
                safe_duration_factor,
                safe_duration_offset,
                tts_stop_headsign,
                min_arrival_time,
                max_departure_time
            FROM stop_times
            ORDER BY trip_id, stop_sequence
            LIMIT %s;
        """, (limit,))

        rows = cursor.fetchall()

        stop_times = []

        for row in rows:
            stop_times.append({
                "trip_id": row[0],
                "arrival_time": row[1],
                "departure_time": row[2],
                "stop_id": row[3],
                "stop_sequence": row[4],
                "stop_headsign": row[5],
                "pickup_type": row[6],
                "drop_off_type": row[7],
                "shape_dist_traveled": row[8],
                "timepoint": row[9],
                "start_service_area_id": row[10],
                "end_service_area_id": row[11],
                "start_service_area_radius": row[12],
                "end_service_area_radius": row[13],
                "continuous_pickup": row[14],
                "continuous_drop_off": row[15],
                "pickup_booking_rule_id": row[16],
                "drop_off_booking_rule_id": row[17],
                "start_pickup_drop_off_window": row[18],
                "end_pickup_drop_off_window": row[19],
                "mean_duration_factor": row[20],
                "mean_duration_offset": row[21],
                "safe_duration_factor": row[22],
                "safe_duration_offset": row[23],
                "tts_stop_headsign": row[24],
                "min_arrival_time": row[25],
                "max_departure_time": row[26]
            })

        return stop_times

    finally:
        cursor.close()
        connection.close()
from database.connection import get_connection

from etl.extract import (
    extract_agency,
    extract_routes,
    extract_stops,
    extract_trips,
    extract_stop_times
)

from etl.transform import transform

from etl.load import (
    load_agency,
    load_routes,
    load_stops,
    load_trips,
    load_stop_times
)


def main():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # --------------------
        # Agency
        # --------------------
        agency_df = extract_agency()
        agency_df = transform(agency_df)
        load_agency(cursor, agency_df)

        print("Agency data loaded successfully.")


        # --------------------
        # Routes
        # --------------------
        routes_df = extract_routes()
        routes_df = transform(routes_df)
        load_routes(cursor, routes_df)

        print("Routes data loaded successfully.")


        # --------------------
        # Stops
        # --------------------
        stops_df = extract_stops()
        stops_df = transform(stops_df)
        load_stops(cursor, stops_df)

        print("Stops data loaded successfully.")


        # --------------------
        # Trips
        # --------------------
        trips_df = extract_trips()
        trips_df = transform(trips_df)
        load_trips(cursor, trips_df)

        print("Trips data loaded successfully.")


        # --------------------
        # Stop Times
        # --------------------
        stop_times_df = extract_stop_times()
        stop_times_df = transform(stop_times_df)
        load_stop_times(cursor, stop_times_df)

        print("Stop times data loaded successfully.")


        # Commit everything
        connection.commit()

        print("\nAll GTFS data loaded successfully!")


    except Exception as e:
        connection.rollback()
        print(f"Error loading GTFS data: {e}")
        raise


    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
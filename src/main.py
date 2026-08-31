# src/main.py

from database.connection import get_connection

from etl.extract import extract_agency
from etl.transform import transform
from etl.load import load_agency


AGENCY_FILE = "data/agency.txt"


def main():

    # Extract
    agency_df = extract_agency()

    # Transform
    agency_df = transform(agency_df)

    # Load
    connection = get_connection()

    try:
        cursor = connection.cursor()

        load_agency(cursor, agency_df)

        connection.commit()

        print("Agency data loaded successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error loading agency data: {e}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
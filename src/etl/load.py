from database.connection import get_connection

def load_agency(df):
    connection = get_connection()
    cursor = connection.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO agency (
                agency_id,
                agency_name,
                agency_url,
                agency_timezone,
                agency_lang
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                row["agency_id"],
                row["agency_name"],
                row["agency_url"],
                row["agency_timezone"],
                row["agency_lang"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()
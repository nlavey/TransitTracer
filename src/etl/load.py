# src/etl/load.py

from psycopg2 import sql


def get_existing_columns(cursor, table_name):
    """
    Get the columns currently in a PostgreSQL table.
    """
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))

    return {row[0] for row in cursor.fetchall()}


def add_missing_columns(cursor, table_name, columns):
    """
    Add any DataFrame columns that don't exist in the database table.
    New columns are initially created as TEXT.
    """

    existing_columns = get_existing_columns(cursor, table_name)

    for column in columns:
        if column not in existing_columns:

            query = sql.SQL(
                'ALTER TABLE {} ADD COLUMN {} TEXT'
            ).format(
                sql.Identifier(table_name),
                sql.Identifier(column)
            )

            cursor.execute(query)

            print(
                f"Added missing column '{column}' "
                f"to table '{table_name}'"
            )


def load_dataframe(cursor, table_name, df):
    """
    Add missing columns and insert DataFrame rows.
    """

    # Make sure the database has every column
    add_missing_columns(
        cursor,
        table_name,
        df.columns
    )

    columns = list(df.columns)

    column_names = sql.SQL(", ").join(
        sql.Identifier(column)
        for column in columns
    )

    placeholders = sql.SQL(", ").join(
        sql.Placeholder()
        for _ in columns
    )

    query = sql.SQL("""
        INSERT INTO {} ({})
        VALUES ({})
    """).format(
        sql.Identifier(table_name),
        column_names,
        placeholders
    )

    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)


def load_agency(cursor, df):
    """
    Load agency data into the agency table.
    """
    load_dataframe(cursor, "agency", df)


def load_routes(cursor, df):
    """
    Load routes data into the routes table.
    """
    load_dataframe(cursor, "routes", df)


def load_stops(cursor, df):
    """
    Load stops data into the stops table.
    """
    load_dataframe(cursor, "stops", df)


def load_trips(cursor, df):
    """
    Load trips data into the trips table.
    """
    load_dataframe(cursor, "trips", df)


def load_stop_times(cursor, df):
    """
    Load stop_times data into the stop_times table.
    """
    load_dataframe(cursor, "stop_times", df)
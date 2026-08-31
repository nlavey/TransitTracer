import psycopg2
from psycopg2 import sql


def get_existing_columns(cursor, table_name):
    """
    Get the columns that currently exist in a PostgreSQL table.
    """
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))

    return {row[0] for row in cursor.fetchall()}


def add_missing_columns(cursor, table_name, columns):
    """
    Add columns from the DataFrame that don't exist in the database.
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


def load_dataframe(cursor, table_name, df, conflict_columns):
    """
    Add missing columns and insert/update DataFrame rows.
    """

    # Make sure every DataFrame column exists in the database
    add_missing_columns(
        cursor,
        table_name,
        df.columns
    )

    columns = list(df.columns)

    # Column names for INSERT
    column_names = sql.SQL(", ").join(
        sql.Identifier(column)
        for column in columns
    )

    # %s placeholders
    placeholders = sql.SQL(", ").join(
        sql.Placeholder()
        for _ in columns
    )

    # Columns that should be updated if a conflict occurs
    update_columns = [
        column
        for column in columns
        if column not in conflict_columns
    ]

    # Build UPDATE portion
    if update_columns:
        update_clause = sql.SQL(", ").join(
            sql.SQL("{} = EXCLUDED.{}").format(
                sql.Identifier(column),
                sql.Identifier(column)
            )
            for column in update_columns
        )
    else:
        update_clause = sql.SQL("NOTHING")

    # Composite or single-column conflict key
    conflict_clause = sql.SQL(", ").join(
        sql.Identifier(column)
        for column in conflict_columns
    )

    # Build query
    if update_columns:
        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({})
            ON CONFLICT ({})
            DO UPDATE SET {}
        """).format(
            sql.Identifier(table_name),
            column_names,
            placeholders,
            conflict_clause,
            update_clause
        )
    else:
        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({})
            ON CONFLICT ({})
            DO NOTHING
        """).format(
            sql.Identifier(table_name),
            column_names,
            placeholders,
            conflict_clause
        )

    # Insert each row
    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)


# --------------------------------------------------
# Individual table loaders
# --------------------------------------------------

def load_agency(cursor, df):
    load_dataframe(
        cursor,
        "agency",
        df,
        ["agency_id"]
    )


def load_routes(cursor, df):
    load_dataframe(
        cursor,
        "routes",
        df,
        ["route_id"]
    )


def load_stops(cursor, df):
    load_dataframe(
        cursor,
        "stops",
        df,
        ["stop_id"]
    )


def load_trips(cursor, df):
    load_dataframe(
        cursor,
        "trips",
        df,
        ["trip_id"]
    )


def load_stop_times(cursor, df):
    load_dataframe(
        cursor,
        "stop_times",
        df,
        ["trip_id", "stop_sequence"]
    )
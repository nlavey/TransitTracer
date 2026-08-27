def clean_agency(df):
    df = df.copy()

    # Remove leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing whitespace from string values
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    return df


def clean_routes(df):
    df = df.copy()

    df.columns = df.columns.str.strip()

    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    return df


def clean_stops(df):
    df = df.copy()

    df.columns = df.columns.str.strip()

    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    return df


def clean_trips(df):
    df = df.copy()

    df.columns = df.columns.str.strip()

    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    return df


def clean_stop_times(df):
    df = df.copy()

    df.columns = df.columns.str.strip()

    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    return df
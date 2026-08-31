# src/etl/transform.py

import pandas as pd


def clean_columns(df):
    """
    Clean column names.
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df


def clean_values(df):
    """
    Clean string values and convert empty values to None.
    """
    df = df.copy()

    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    df = df.where(pd.notna(df), None)

    return df


def transform(df):
    """
    Run all transformations.
    """
    df = clean_columns(df)
    df = clean_values(df)

    return df
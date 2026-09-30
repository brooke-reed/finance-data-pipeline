"""
transformation.py

Transforms data into valid format for financial database
"""
import polars as pl
from extract import extract_data

def transform_data(df):
    # Normalize whitespace and capitalization
    columns = ["Category", "Type", "Date"]
    for column in columns:
        df = df.with_columns(pl.col(column).str.strip_chars())

    df = df.with_columns(pl.col("Type").str.to_titlecase())
    df = df.with_columns(pl.col("Category").str.to_titlecase())

    # Handle optional cases of descriptions
    if "Transaction Description" in df.columns:
        df = df.with_columns(pl.col("Transaction Description").str.strip_chars())
        df = df.with_columns(pl.when(pl.col("Transaction Description") == "")
                              .then(pl.lit(None))
                              .otherwise(pl.col("Transaction Description")).alias("Transaction Description"))
    else:
        df = df.with_columns(pl.lit(None).alias("Transaction Description"))


    # Convert Strings to data types
    df = df.with_columns(pl.col("Date").str.to_date())
    return df

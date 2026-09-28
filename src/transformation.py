"""
transformation.py

Transforms data into valid format for financial database
"""
import polars as pl
from extract import extract_data
from data_validation import validate_data

def transform_data(df):
    # Normalize whitespace and capitalization
    columns = ["Category", "Type", "Date"]
    for column in columns:
        df = df.with_columns(pl.col(column).str.strip_chars())
    df = df.with_columns(pl.col("Type").str.to_titlecase())
    df = df.with_columns(pl.col("Category").str.to_titlecase())
    if "Transaction Description" in df.columns:
        df = df.with_columns(pl.col("Transaction Description").str.strip_chars())

    # Convert Strings to data types
    df = df.with_columns(pl.col("Date").str.to_date())
    return df



if __name__ == "__main__":
    # Testing

    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(pl.lit(" 2024-09-21 ")).otherwise(pl.col("Date")).alias("Date")])
    df = df.with_columns([pl.when(pl.col("index") == 3).then(pl.lit("    inCOme  ")).otherwise(pl.col("Type")).alias("Type")])
    df = df.with_columns([pl.when(pl.col("index") == 3).then(pl.lit("   FOOd & drINK ")).otherwise(pl.col("Category")).alias("Category")])
    df = df.with_columns([pl.when(pl.col("index") == 3).then(pl.lit("  Grocery shopping ")).otherwise(pl.col("Transaction Description")).alias("Transaction Description")])
    df = df.drop("index")
    print(transform_data(df))
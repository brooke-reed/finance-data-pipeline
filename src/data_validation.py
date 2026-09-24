"""
data_validation.py

Validates data from a CSV file to be imported into financial tracker database
"""

import polars as pl
from extract import extract_data

def validate_data(df):
    """
    Takes a DataFrame and returns True/False with errors 
    depending on whether data is valid
    """
    errors = []
    # Check all required columns present
    required_columns = ["Amount", "Category", "Type", "Date"]
    missing_columns = []
    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if len(missing_columns) > 0:
        errors.append(f"Missing columns {missing_columns}")
        return len(errors) == 0, errors

    # Data Checks 
    # No nulls (except descriptions)
    null_columns = []
    null_df = df.null_count()
    for column in required_columns:
        if null_df[column][0] > 0:
            null_columns.append(column)

    if len(null_columns) > 0:
        errors.append(f"Null values found in columns {null_columns}")

    # Data meets constraints of character limits in Category
    if not (df.select((pl.col("Category").str.len_chars() <= 50).all()).item()):
        errors.append("Category names must be up to 50 characters")

    # Amounts must be greater than 0
    if not (df.select((pl.col("Amount") > 0).all()).item()):
        errors.append("All amount values must be positive")
    
    # Dates are formatted correctly
    date_check = df.with_columns(dates = pl.col("Date").str.to_date("%Y-%m-%d", strict=False))
    null_df = date_check.null_count()
    if null_df["dates"][0] > 0:
        errors.append("Dates must be formatted as YEAR-MONTH-DAY")
    
    # Validate type is only income or expense
    valid_types = ["Income", "Expense"]
    if not (df.select(pl.col("Type").is_in(valid_types).all()).item()):
        errors.append("Transaction type must be either Income or Expense")

    return len(errors) == 0, errors

    

if __name__ == "__main__":
    #Testing

    #Correct dataset
    print(validate_data(extract_data("data/raw/Personal_Finance_Dataset.csv")))

    #"Broken" dataset

    #Missing column
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.drop("Type")
    print(validate_data(df))

    #Includes nulls
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(None).otherwise(pl.col("Amount")).alias("Amount")])
    print(validate_data(df))

    #Includes negative amounts
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(-3).otherwise(pl.col("Amount")).alias("Amount")])
    print(validate_data(df))

    #Invalid date format
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(pl.lit("str")).otherwise(pl.col("Date")).alias("Date")])
    print(validate_data(df))

    #Type column is not valid
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(pl.lit("Other")).otherwise(pl.col("Type")).alias("Type")])
    print(validate_data(df))

    #Character limit is exceeded
    df = extract_data("data/raw/Personal_Finance_Dataset.csv")
    df = df.with_row_index().with_columns([pl.when(pl.col("index") == 3).then(pl.lit("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")).otherwise(pl.col("Category")).alias("Category")])
    print(validate_data(df))
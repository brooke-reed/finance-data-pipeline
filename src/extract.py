# Extracting data from user uploaded CSV file
# Future update: allow for file upload or individual adding of transactions

import polars as pl

def extract_data(csv):
    df = pl.read_csv(csv)
    return df
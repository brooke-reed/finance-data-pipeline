# used to explore data sets
import polars as pl

df = pl.read_csv("data/raw/Personal_Finance_Dataset.csv")
#explore dataset on first five lines
print(df.head(5))
#determine size of dataset
print("Shape of dataset")
print(df.shape)
#determine amount of nulls
print("Number of nulls")
print(df.null_count())
#determine unique types
print("Unique Categories")
print(df["Category"].unique())
print(df["Category"].value_counts())

print("Unique Types")
print(df["Type"].unique())
print(df["Type"].value_counts())

#transaction bound exploration
print("Max and Min transactions")
print(df["Amount"].max())
print(df["Amount"].min())

#min and max description lengths
print("Max and Min Description Lengths")
print(df["Transaction Description"].str.len_chars().max())
print(df["Transaction Description"].str.len_chars().min())

#oldest and newest date
print("Newest and Oldest Date")
print(df["Date"].str.to_date().max())
print(df["Date"].str.to_date().min())

#duplicate rows?
print(df.unique().shape)

#how do categories interact with types?
print(df.group_by("Category").agg(pl.col("Type").unique()))
print(df.group_by("Category").agg(pl.col("Type").value_counts()))
"""
main.py

Driver of finance tracker application
"""
from extract import extract_data
from data_validation import validate_data
from data_validation import validate_structure
from transformation import transform_data
from load import load_data

def main():
    file_path = input("Enter folder path to CSV file: ").strip()
    try:
        df = extract_data(file_path)
    except FileNotFoundError:
        print("File cannot be found")
        return

    # Pre-check necessary constraints on raw data
    is_valid, errors = validate_structure(df)
    if not is_valid:
        print(f"CSV is invalid: {errors}")
        return

    df = transform_data(df)

    # Check rest of constraints
    is_valid, errors = validate_data(df)
    if not is_valid:
        print(f"CSV is not valid: {errors}")
        return

    # Load transformed data to PostgreSQL Database
    is_loaded, error = load_data(df, 1)
    if is_loaded:
        print("Data successfully loaded")
    else :
        print(f"Data load unsuccessful: {error}")


if __name__ == "__main__":
    main()
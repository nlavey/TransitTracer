from etl.extract import extract_agency
from etl.transform import clean_agency
from etl.load import load_agency


def main():
    
    # Extract
    agency = extract_agency()

    print("Extracted agency data:")
    print(agency)

    # Transform
    agency = clean_agency(agency)

    print("\nCleaned agency data:")
    print(agency)

    # Load
    load_agency(agency)

    print("\nAgency data loaded successfully!")


if __name__ == "__main__":
    main()
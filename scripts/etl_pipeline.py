import pandas as pd
import numpy as np
import os


def extract_data():
    """
    Extract phase:
    Load all raw datasets from the data/raw directory.
    """
    df_ticket = pd.read_csv("data/raw/airline_ticket_prices.csv")
    df_fuel = pd.read_csv("data/raw/oil_jet_fuel_prices.csv")
    df_surcharge = pd.read_csv("data/raw/fuel_surcharges.csv")
    
    return df_ticket, df_fuel, df_surcharge


def transform_data(df_ticket, df_fuel, df_surcharge):
    """
    Transform phase:
    Clean, merge, and engineer features from raw datasets.
    """

    # Standardize column names (lowercase + remove spaces)
    for df in [df_ticket, df_fuel, df_surcharge]:
        df.columns = df.columns.str.strip().str.lower()

    # Merge datasets on common keys (month + conflict phase)
    df = df_ticket.merge(df_fuel, on=["month", "conflict_phase"], how="left")

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Handle missing values (simple strategy: fill with 0)
    df.fillna(0, inplace=True)

    # Convert 'month' to datetime and extract useful time features
    df["month"] = pd.to_datetime(df["month"])
    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month

    # Feature Engineering
    # Fare per km → pricing efficiency metric
    df["fare_per_km"] = df["total_fare_usd"] / df["avg_route_km"]

    # Fuel ratio → how much surcharge contributes to total fare
    df["fuel_ratio"] = df["fuel_surcharge_usd"] / df["total_fare_usd"]

    # Outlier flag → identify extreme fare values (do not remove)
    df["is_extreme_fare"] = (
        (df["total_fare_usd"] > df["total_fare_usd"].quantile(0.99)) |
        (df["total_fare_usd"] < df["total_fare_usd"].quantile(0.01))
    )

    return df


def load_data(df):
    """
    Load phase:
    Save the final processed dataset into data/processed directory.
    """

    # Create folder if it does not exist
    os.makedirs("data/processed", exist_ok=True)

    # Save final dataset
    df.to_csv("data/processed/final_dataset.csv", index=False)


def main():
    """
    Main pipeline:
    Executes Extract → Transform → Load in sequence.
    """
    df_ticket, df_fuel, df_surcharge = extract_data()
    df = transform_data(df_ticket, df_fuel, df_surcharge)
    load_data(df)

    print("ETL pipeline executed successfully ✅")


if __name__ == "__main__":
    main()
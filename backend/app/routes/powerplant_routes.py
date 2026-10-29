import pandas as pd
from app.logger import get_logger
from fastapi import APIRouter, Query

router = APIRouter(prefix="/dashboard_powerplant", tags=["Powerplant Dashboard"])
logger = get_logger(__name__)

max_workers = 5
df = None


def get_dataframe():
    global df
    if df is None:
        df = pd.read_csv("data/global_power_plant.csv")

    return df


# a. /energy-capacity
@router.get("/energy_capacity")
def energy_capacity():
    # Return the Top 20 countries sorted by capacity.
    df = get_dataframe()
    country_capacity = df.groupby("country_long")["capacity_mw"].sum()
    top_20 = country_capacity.sort_values(ascending=False).head(20)

    result = [
        {"Country": country, "Total_Installed_Capacity": int(capacity)}
        for country, capacity in top_20.items()
    ]

    return result


# b. /energy-trends
@router.get("/energy_trends")
def energy_trends():
    # Calculate total commissioned capacity for each year.
    df = get_dataframe()

    df = df.dropna(subset =["commissioning_year"])
    df["commissioning_year"] = df["commissioning_year"].astype(int)
    annual_capacity = df.groupby("commissioning_year")["capacity_mw"].sum()

    result = [
        {
            "Year": int(year),
            "Capacity": capacity
        }for year , capacity in annual_capacity.items()
    ]

    return result


# c. /country-insights
@router.get("/country_insights")
def country_insights():
    # Return the Top 15 countries by total installed capacity.
    df = get_dataframe()
    country_capacity = df.groupby("country_long")["capacity_mw"].sum()
    top_15 = country_capacity.sort_values(ascending=False).head(15)

    result = [
        {
            "Country" : country,
            "Capacity" : int(capacity)
        }for country , capacity in top_15.items()
    ]
    return result


# d. /energy-sources
@router.get("/energy_sources")
def energy_sources():
    # Count the number of power plants for each primary fuel.
    df = get_dataframe()
    fuel_count = df["primary_fuel"].value_counts().to_dict()

    return fuel_count
    

"""
Direct data queries on the CSV for aggregation questions.
RAG is good for specific plant lookups, but for counting/listing all plants
in a country or listing fuel types, we query the dataset directly.
"""
import pandas as pd
import os
from app.logger import get_logger

logger = get_logger(__name__)

_df = None
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/cleaned_dataset.csv")


def get_df():
    global _df
    if _df is None:
        _df = pd.read_csv(DATA_PATH)
        _df["country_long"] = _df["country_long"].str.strip().str.lower()
        _df["country"] = _df["country"].str.strip().str.upper()
        _df["primary_fuel"] = _df["primary_fuel"].str.strip()
    return _df


# Keywords that signal aggregation intent
COUNT_KEYWORDS = ["how many", "count", "number of", "total"]
LIST_KEYWORDS = ["list", "name all", "all plants", "which plants", "what plants"]
TYPE_KEYWORDS = ["types of", "what type", "kinds of", "fuel type", "energy source", "what kind"]
CAPACITY_KEYWORDS = ["capacity", "largest", "biggest", "highest capacity", "most powerful"]


def detect_country(question: str) -> str | None:
    """Try to find a country name mentioned in the question."""
    df = get_df()
    q = question.lower()
    # Check full country names first (longer match wins)
    countries = df["country_long"].unique()
    countries_sorted = sorted(countries, key=len, reverse=True)
    for c in countries_sorted:
        if c and c in q:
            return c
    return None


def classify_question(question: str) -> str:
    """Returns: 'count', 'list', 'types', 'capacity', or 'rag'"""
    q = question.lower()
    if any(k in q for k in TYPE_KEYWORDS):
        return "types"
    if any(k in q for k in COUNT_KEYWORDS):
        return "count"
    if any(k in q for k in LIST_KEYWORDS):
        return "list"
    if any(k in q for k in CAPACITY_KEYWORDS):
        return "capacity"
    return "rag"


def answer_from_data(question: str) -> str | None:
    """
    Returns a direct data answer if the question is an aggregation query.
    Returns None if it should fall through to RAG.
    """
    intent = classify_question(question)
    country = detect_country(question)
    df = get_df()

    # --- Types / fuel types question (no country needed) ---
    if intent == "types":
        if country:
            subset = df[df["country_long"] == country]
            fuels = subset["primary_fuel"].value_counts()
        else:
            fuels = df["primary_fuel"].value_counts()

        if fuels.empty:
            return None

        lines = [f"  - {fuel}: {count} plants" for fuel, count in fuels.items()]
        scope = country.title() if country else "the world"
        return f"Power plant fuel types in {scope}:\n" + "\n".join(lines)

    # --- Count question ---
    if intent == "count" and country:
        subset = df[df["country_long"] == country]
        total = len(subset)
        if total == 0:
            return f"No power plants found for '{country.title()}' in the dataset."
        fuel_breakdown = subset["primary_fuel"].value_counts()
        lines = [f"  - {fuel}: {cnt}" for fuel, cnt in fuel_breakdown.items()]
        return (
            f"There are {total} power plants in {country.title()}.\n"
            f"Breakdown by fuel type:\n" + "\n".join(lines)
        )

    # --- List question ---
    if intent == "list" and country:
        subset = df[df["country_long"] == country]
        total = len(subset)
        if total == 0:
            return f"No power plants found for '{country.title()}' in the dataset."
        names = subset["name"].tolist()
        lines = [f"  {i+1}. {name}" for i, name in enumerate(names)]
        return (
            f"All {total} power plants in {country.title()}:\n" + "\n".join(lines)
        )

    # --- Capacity question ---
    if intent == "capacity" and country:
        subset = df[df["country_long"] == country]
        if subset.empty:
            return None
        subset = subset[subset["capacity_mw"] != ""].copy()
        subset["capacity_mw"] = pd.to_numeric(subset["capacity_mw"], errors="coerce")
        top = subset.nlargest(10, "capacity_mw")[["name", "capacity_mw", "primary_fuel"]]
        lines = [
            f"  {i+1}. {row['name']} — {row['capacity_mw']} MW ({row['primary_fuel']})"
            for i, row in enumerate(top.to_dict("records"))
        ]
        return f"Top power plants by capacity in {country.title()}:\n" + "\n".join(lines)

    # Fall through to RAG
    return None

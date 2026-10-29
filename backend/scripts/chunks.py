import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "..", "data", "cleaned_dataset.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "data", "chunks.csv")


def create_chunk_text(row):
    return (
        f"The power plant named '{row.get('name', 'Unknown')}' is located in "
        f"{row.get('country_long', 'unknown')} ({row.get('country', 'unknown')}). "
        f"It uses {row.get('primary_fuel', 'unknown')} as primary fuel and has an "
        f"installed capacity of {row.get('capacity_mw', 'N/A')} MW. "
        f"Coordinates: latitude {row.get('latitude', 'N/A')}, longitude {row.get('longitude', 'N/A')}."
    )


def create_chunks():
    df = pd.read_csv(INPUT_FILE)
    chunk_records = []

    for idx, row in df.iterrows():
        chunk_records.append({
            "chunk_id": idx + 1,
            "chunk_text": create_chunk_text(row),
            "country": row.get("country", ""),
            "country_long": row.get("country_long", ""),
            "name": row.get("name", ""),
            "primary_fuel": row.get("primary_fuel", ""),
            "capacity_mw": row.get("capacity_mw", ""),
        })

    result_df = pd.DataFrame(chunk_records)
    result_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Created {len(chunk_records)} chunks (one per plant) in {OUTPUT_FILE}")
    return result_df


create_chunks()
print(pd.read_csv(OUTPUT_FILE, nrows=3))
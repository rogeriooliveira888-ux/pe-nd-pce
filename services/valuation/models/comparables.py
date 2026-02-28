import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SECTOR_FILE = PROJECT_ROOT / "data" / "sector_multiples.csv"

def run_comparables(path, sector="mining"):
    df = pd.read_csv(path)
    sector_df = pd.read_csv(SECTOR_FILE)

    multiple = sector_df.loc[
        sector_df["sector"]==sector,"multiple"
    ].values[0]

    ebitda = df["EBITDA"].iloc[-1]
    return ebitda * multiple
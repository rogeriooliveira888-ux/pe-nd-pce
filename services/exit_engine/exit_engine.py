from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"

TARGET_IRR = 0.25
MIN_GROWTH = 0.03

def load_data(path):
    return pd.read_csv(path)

def suggest_exit(current_irr, growth):
    if current_irr >= TARGET_IRR:
        return "VENDER AGORA"

    if growth < MIN_GROWTH:
        return "VENDER - EMPRESA PERDENDO FORCA"

    if current_irr > 0.18:
        return "PREPARAR EXIT EM 12-24 MESES"

    return "MANTER INVESTIMENTO"

def run_exit_engine(path, irr):
    df = load_data(path)
    growth = df["Revenue"].pct_change().iloc[-1]
    decision = suggest_exit(irr, growth)

    return {
        "Current_IRR": irr,
        "Growth": growth,
        "Exit_Decision": decision
    }

if __name__ == "__main__":
    example_irr = 0.22
    result = run_exit_engine(DATA_PATH, example_irr)
    print(result)
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "real" / "vale.csv"

def load_data(path):
    return pd.read_csv(path)

def project(base, growth, years):
    return [base*(1+growth)**i for i in range(1, years+1)]

def run_scenario(df, ebitda_growth, fcf_growth, entry_mult, exit_mult):
    base_ebitda = df["EBITDA"].iloc[-1]
    base_fcf = df["FCF"].iloc[-1]

    entry = base_ebitda * entry_mult
    debt = entry * 0.6
    equity = entry - debt

    ebitda_proj = project(base_ebitda, ebitda_growth, 5)

    fcf = base_fcf
    for _ in ebitda_proj:
        fcf *= (1+fcf_growth)
        debt -= fcf
        if debt < 0:
            debt = 0

    exit_equity = ebitda_proj[-1] * exit_mult - debt
    irr = (exit_equity/equity)**(1/5)-1

    return irr

def run_lbo(path=DATA_PATH):
    df = load_data(path)

    return {
        "Pessimista": run_scenario(df,0.03,0.02,8,8),
        "Base": run_scenario(df,0.07,0.05,8,9),
        "Otimista": run_scenario(df,0.10,0.08,8,10),
    }

if __name__ == "__main__":
    print(run_lbo())
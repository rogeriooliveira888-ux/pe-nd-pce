from pathlib import Path
import pandas as pd

# =====================================================
# Detectar raiz do projeto automaticamente
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"

# =====================================================
# Parâmetros do fundo
# =====================================================
MIN_IRR = 0.20
MAX_LEVERAGE = 5
MIN_MARGIN = 0.15
MIN_GROWTH = 0.05


def load_data(path):
    return pd.read_csv(path)


def calculate_basic_metrics(df):
    growth = df["Revenue"].pct_change().mean()
    margin = (df["EBITDA"] / df["Revenue"]).mean()
    leverage = df["Net_Debt"].iloc[-1] / df["EBITDA"].iloc[-1]
    return growth, margin, leverage


def decide_investment(irr, growth, margin, leverage):
    if irr >= MIN_IRR and leverage <= MAX_LEVERAGE \
       and margin >= MIN_MARGIN and growth >= MIN_GROWTH:
        return "INVESTIR"
    else:
        return "NAO INVESTIR"


def run_decision(path, irr):
    df = load_data(path)
    growth, margin, leverage = calculate_basic_metrics(df)
    decision = decide_investment(irr, growth, margin, leverage)

    return {
        "Growth": growth,
        "Margin": margin,
        "Leverage": leverage,
        "IRR": irr,
        "Decision": decision
    }


if __name__ == "__main__":
    example_irr = 0.22
    result = run_decision(DATA_PATH, example_irr)
    print(result)
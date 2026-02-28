from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"

# Limites do fundo
MAX_LEVERAGE = 5
MIN_GROWTH = 0.03
MIN_MARGIN = 0.10

def load_data(path):
    return pd.read_csv(path)

def calculate_metrics(df):
    revenue_growth = df["Revenue"].pct_change().iloc[-1]
    ebitda_margin = (df["EBITDA"] / df["Revenue"]).iloc[-1]
    leverage = df["Net_Debt"].iloc[-1] / df["EBITDA"].iloc[-1]
    return revenue_growth, ebitda_margin, leverage

def portfolio_alerts(growth, margin, leverage):
    alerts = []

    if growth < MIN_GROWTH:
        alerts.append("CRESCIMENTO BAIXO")

    if margin < MIN_MARGIN:
        alerts.append("MARGEM BAIXA")

    if leverage > MAX_LEVERAGE:
        alerts.append("DIVIDA ALTA")

    if not alerts:
        alerts.append("EMPRESA SAUDAVEL")

    return alerts

def run_monitor(path):
    df = load_data(path)
    growth, margin, leverage = calculate_metrics(df)
    alerts = portfolio_alerts(growth, margin, leverage)

    return {
        "Growth": growth,
        "Margin": margin,
        "Leverage": leverage,
        "Alerts": alerts
    }

if __name__ == "__main__":
    result = run_monitor(DATA_PATH)
    print(result)
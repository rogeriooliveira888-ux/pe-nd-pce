from pathlib import Path
import pandas as pd

# Detectar raiz do projeto automaticamente
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"


def load_company_data(path):
    return pd.read_csv(path)


def revenue_growth(df):
    df["Revenue_Growth"] = df["Revenue"].pct_change()
    return df


def margins(df):
    df["Gross_Margin"] = (df["Revenue"] - df["COGS"]) / df["Revenue"]
    df["EBITDA_Margin"] = df["EBITDA"] / df["Revenue"]
    df["Net_Margin"] = df["Net_Income"] / df["Revenue"]
    return df


def free_cash_flow(df):
    df["FCF"] = (
        df["EBIT"] * (1 - df["Tax_Rate"])
        + df["Depreciation"]
        - df["CAPEX"]
        - df["Delta_Working_Capital"]
    )
    return df


def leverage(df):
    df["Leverage"] = df["Net_Debt"] / df["EBITDA"]
    return df


def calculate_all_metrics(path):
    df = load_company_data(path)
    df = revenue_growth(df)
    df = margins(df)
    df = free_cash_flow(df)
    df = leverage(df)
    return df


if __name__ == "__main__":
    result = calculate_all_metrics(DATA_PATH)
    print(result.tail())
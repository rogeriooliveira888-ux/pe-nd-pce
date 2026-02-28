from pathlib import Path
import pandas as pd
import numpy as np
from services.valuation.models.wacc import calculate_wacc

# =====================================================
# Detectar raiz do projeto automaticamente
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"

# =====================================================
# Funções auxiliares
# =====================================================

def load_data(path):
    if not Path(path).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path)


def project_fcf(last_fcf, growth_rate, years):
    projections = []
    fcf = last_fcf
    for _ in range(years):
        fcf *= (1 + growth_rate)
        projections.append(fcf)
    return projections


def dcf_valuation(fcfs, discount_rate, terminal_growth):
    value = 0
    for t, fcf in enumerate(fcfs, start=1):
        value += fcf / (1 + discount_rate) ** t

    terminal_value = (
        fcfs[-1] * (1 + terminal_growth)
    ) / (discount_rate - terminal_growth)

    terminal_discounted = terminal_value / (1 + discount_rate) ** len(fcfs)

    return value + terminal_discounted


# =====================================================
# CENÁRIOS PROFISSIONAIS
# =====================================================

def run_scenario(last_fcf, equity, debt, growth, terminal_growth):
    fcfs = project_fcf(last_fcf, growth, 5)
    discount_rate = calculate_wacc(equity, debt)
    return dcf_valuation(fcfs, discount_rate, terminal_growth)


# =====================================================
# EXECUÇÃO PRINCIPAL
# =====================================================

def run_dcf(path):
    df = load_data(path)

    if "FCF" not in df.columns:
        raise ValueError("Coluna FCF não encontrada no CSV")

    last_fcf = df["FCF"].iloc[-1]

    # Estrutura capital exemplo (ajustaremos depois)
    equity = 100
    debt = 50

    pessimista = run_scenario(last_fcf, equity, debt, 0.02, 0.01)
    base = run_scenario(last_fcf, equity, debt, 0.05, 0.02)
    otimista = run_scenario(last_fcf, equity, debt, 0.08, 0.03)

    return {
        "Pessimista": pessimista,
        "Base": base,
        "Otimista": otimista
    }


# =====================================================
# Execução direta
# =====================================================
if __name__ == "__main__":
    print("Usando arquivo:", DATA_PATH)
    result = run_dcf(DATA_PATH)
    print("DCF Cenários:")
    for k, v in result.items():
        print(f"{k}: {v:,.2f}")
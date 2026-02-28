from pathlib import Path
import pandas as pd

# ============================================
# Detectar raiz do projeto
# ============================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "examples" / "company_example.csv"

# ============================================
# Importar LBO
# ============================================
import sys
sys.path.append(str(PROJECT_ROOT))

from services.lbo.models.lbo import run_lbo
from services.decision.investment_decision import run_decision


# ============================================
# Execução integrada
# ============================================
def run_full_analysis():
    lbo_result = run_lbo(DATA_PATH)
    irr = lbo_result["IRR"]

    decision_result = run_decision(DATA_PATH, irr)

    return {
        "LBO": lbo_result,
        "Decision": decision_result
    }


if __name__ == "__main__":
    result = run_full_analysis()
    print(result)
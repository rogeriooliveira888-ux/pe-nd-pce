import streamlit as st
from pathlib import Path

from services.valuation.models.dcf import run_dcf
from services.valuation.models.comparables import run_comparables
from services.lbo.models.lbo import run_lbo
from services.decision.investment_decision import run_decision
from services.portfolio.monitor import run_monitor
from services.exit_engine.exit_engine import run_exit_engine
from services.reports.report import generate_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data/real/vale.csv"

st.title("PE-ND-PCE Dashboard")

# ===============================
# VALUATION
# ===============================
st.header("Valuation")

dcf = run_dcf(DATA_PATH)
comp_value = run_comparables(DATA_PATH)

st.subheader("DCF Cenários")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pessimista", f"{dcf['Pessimista']:,.0f}")

with col2:
    st.metric("Base", f"{dcf['Base']:,.0f}")

with col3:
    st.metric("Otimista", f"{dcf['Otimista']:,.0f}")

st.metric("Comparables", f"{comp_value:,.0f}")

# ===============================
# LBO
# ===============================
st.header("LBO")
lbo = run_lbo(DATA_PATH)
st.write(lbo)

# pegar IRR corretamente
if isinstance(lbo, dict) and "IRR" in lbo:
    irr_value = lbo["IRR"]
else:
    # se for cenários
    irr_value = list(lbo.values())[1]  # cenário base

# ===============================
# DECISION
# ===============================
st.header("Decision")
decision = run_decision(DATA_PATH, irr_value)
st.write(decision)

# ===============================
# MONITORAMENTO
# ===============================
st.header("Portfolio Monitoring")
monitor = run_monitor(DATA_PATH)
st.write(monitor)

# ===============================
# EXIT
# ===============================
st.header("Exit Suggestion")
exit_decision = run_exit_engine(DATA_PATH, irr_value)
st.write(exit_decision)

# ===============================
# RELATÓRIO PDF
# ===============================
st.header("Gerar Relatório")

if st.button("Gerar Relatório PDF"):
    data_report = {
        "DCF": dcf,
        "Comparables": comp_value,
        "LBO": lbo,
        "Decision": decision,
        "Monitor": monitor,
        "Exit": exit_decision,
    }

    generate_report(data_report)
    st.success("Relatório gerado em C:\\Projetos\\PE-ND-PCE\\reports_output")
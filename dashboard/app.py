import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from services.valuation.models.dcf import run_dcf
from services.valuation.models.comparables import run_comparables
from services.lbo.models.lbo import run_lbo
from services.decision.investment_decision import run_decision
from services.portfolio.monitor import run_monitor
from services.exit_engine.exit_engine import run_exit_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data/real/vale.csv"

st.title("PE-ND-PCE Dashboard")

# Verificar arquivo
if not DATA_PATH.exists():
    st.error(f"Arquivo não encontrado: {DATA_PATH}")
    st.stop()

# VALUATION
st.header("Valuation")
dcf = run_dcf(DATA_PATH)
comp_value = run_comparables(DATA_PATH)

col1, col2, col3 = st.columns(3)
col1.metric("Pessimista", f"{dcf['Pessimista']:,.0f}")
col2.metric("Base", f"{dcf['Base']:,.0f}")
col3.metric("Otimista", f"{dcf['Otimista']:,.0f}")
st.metric("Comparables", f"{comp_value:,.0f}")

# LBO
st.header("LBO")
lbo = run_lbo(DATA_PATH)
st.write(lbo)

irr_value = lbo["IRR"] if isinstance(lbo, dict) and "IRR" in lbo else 0.15

# DECISION
st.header("Decision")
st.write(run_decision(DATA_PATH, irr_value))

# MONITOR
st.header("Portfolio Monitoring")
st.write(run_monitor(DATA_PATH))

# EXIT
st.header("Exit Suggestion")
st.write(run_exit_engine(DATA_PATH, irr_value))

st.info("PDF desativado no cloud (somente versão local).")
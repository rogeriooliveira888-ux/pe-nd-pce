import numpy as np
from services.valuation.models.dcf import dcf_valuation, project_fcf

def monte_carlo(last_fcf, discount_rate, terminal_growth, sims=500):
    results = []

    for _ in range(sims):
        growth = np.random.normal(0.05, 0.02)
        fcfs = project_fcf(last_fcf, growth, 5)
        value = dcf_valuation(fcfs, discount_rate, terminal_growth)
        results.append(value)

    return {
        "mean": np.mean(results),
        "min": np.min(results),
        "max": np.max(results),
    }
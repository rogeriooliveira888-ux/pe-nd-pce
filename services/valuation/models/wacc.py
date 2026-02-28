def calculate_wacc(
    equity,
    debt,
    risk_free=0.11,
    beta=1.1,
    market_premium=0.05,
    cost_debt=0.13,
    tax_rate=0.34,
):
    re = risk_free + beta * market_premium
    wacc = (equity/(equity+debt))*re + (debt/(equity+debt))*cost_debt*(1-tax_rate)
    return wacc
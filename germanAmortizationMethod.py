from classes.flow import Flow
from classes.results import Results
from scipy.optimize import newton

def amortization(nominal_value, duration, currentperiod):
    amort = nominal_value / (duration - currentperiod + 1) 
    return amort

def period_Coupon(nominal_value, coupon_rate):
    return nominal_value * coupon_rate

def period_Fee(nominal_value, amortization, coupon_rate):
    return amortization + period_Coupon(nominal_value, coupon_rate)


def initial_Costs(commercial_value, flotation, cavali_cost):
    return commercial_value + (flotation*commercial_value) + (cavali_cost*commercial_value)

def TIR(value, flows):
    def npv(rate):
        return sum(flow.net_flow / ((1 + rate) ** flow.period) for flow in flows) - value
    try:
        return newton(npv, 0.05)  # Initial guess of 5%
    except:
        return None 

def TCEA(bond, flows):
    initial_costs=bond.nominal_value + (bond.structuration*bond.nominal_value) + (bond.colocation*bond.nominal_value)
    tcea = ((1+TIR(initial_costs, flows)) ** bond.payment_frequency) - 1
    return tcea

def TREA(bond,flows):
    initial_costs=bond.commercial_value + (bond.flotation*bond.commercial_value) + (bond.cavali*bond.commercial_value)
    trea = ((1+TIR(initial_costs, flows)) ** bond.payment_frequency) - 1
    return trea

def COK(market_rate, duration, payment_frequency):
    return (1 + market_rate) ** (120 / 30) - 1

def max_price(flows, cok):
    price = 0
    for flow in flows:
        price += flow.net_flow / (1 + cok) ** flow.period
    return price


def german_Amortization_Method(bond):
    flows = []
    initial_balance = bond.nominal_value
    bonus= 0
    for period in range(1, bond.duration + 1):

        coupon = period_Coupon(initial_balance, bond.coupon_rate)
        constant_amortization = amortization(initial_balance, bond.duration, period)
        
        # Período de gracia total - no se paga nada, pero balance se calcula normalmente
        if period <= bond.total_grace_period:
            constant_amortization = 0
            net_flow = 0.0
            final_balance = initial_balance + coupon# Balance se calcula normalmente
        
        # Período de gracia parcial - se paga normal pero balance se mantiene estático
        elif period <= (bond.total_grace_period + bond.partial_grace_period):
            constant_amortization = 0
            net_flow = constant_amortization + coupon  # Se calcula como período normal
            final_balance = initial_balance  # Balance se mantiene estático
        
        # Período normal
        else:
            if period == bond.duration:
                bonus = bond.bonus * initial_balance
                net_flow = bonus + constant_amortization + coupon
                final_balance = 0.0
            else:
                net_flow = period_Fee(final_balance, constant_amortization, bond.coupon_rate)
                final_balance = initial_balance - constant_amortization

        flow = Flow(
            bond.id,  # bond_id, can be set to a unique value or generated
            period,
            initial_balance,
            constant_amortization,  # Solo amortización después de gracia total
            coupon,
            bonus,
            net_flow,
            final_balance
        )
        flows.append(flow)
        
        # Actualizar initial_balance según el tipo de período
        if period <= bond.total_grace_period:
            # En gracia total: balance se calcula normalmente
            initial_balance = final_balance
        elif period <= (bond.total_grace_period + bond.partial_grace_period):
            # En gracia parcial: balance se mantiene estático
            # No se actualiza initial_balance
            pass
        else:
            # Período normal: se actualiza normalmente
            initial_balance = final_balance

    # Calcular TIR, TCEA y TREA
    trea= TREA(bond, flows)
    tcea = TCEA(bond, flows)
    cok = COK(bond.market_rate, bond.duration, bond.payment_frequency)
    max_price_value = max_price(flows, cok)

    results = Results(
        1,  # results_id, can be set to a unique value or generated
        bond.id,
        tcea,
        trea,
        max_price_value
    )


    return flows, results
from models.flow import Flow
from models.results import Results

def amortization(nominal_value, duration):
    return nominal_value / duration 

def period_Coupon(nominal_value, coupon_rate):
    return nominal_value * coupon_rate

def period_Fee(nominal_value, amortization, coupon_rate):
    return amortization + period_Coupon(nominal_value, coupon_rate)

def last_Flow_Bonus(bonus_percentage, period_initial_balance, flow):
    bonus = bonus_percentage * period_initial_balance
    return flow + bonus

def initial_Costs(commercial_value, flotation, cavali_cost):
    return commercial_value + (flotation*commercial_value) + (cavali_cost*commercial_value)

def calculate_cok(market_rate, period, payment_frequency):
    return (1 + market_rate) ** (payment_frequency / period) - 1

def present_value(flow, period, cok):
    return flow / (1 + cok) ** period

def utility(price, final_balance):
    return price - final_balance

def german_Amortization_Method(bond):
    flows = []
    initial_balance = bond.nominal_value
    constant_amortization = amortization(bond.nominal_value, bond.duration)

    for period in range(1, bond.duration + 1):
        coupon = period_Coupon(initial_balance, bond.coupon_rate)
        bonus = 0.0
        if period == bond.duration:
            bonus = bond.redemption_bonus
            net_flow = last_Flow_Bonus(bonus, initial_balance, constant_amortization + coupon)
            final_balance = 0.0
        else:
            net_flow = constant_amortization + coupon
            final_balance = initial_balance - constant_amortization

        flow = Flow(
            1,
            period,
            initial_balance,
            constant_amortization,
            coupon,
            bonus,
            net_flow,
            final_balance
        )
        flows.append(flow)
        initial_balance = final_balance

    r=0
    period = 0
    coks = calculate_cok(bond.market_rate, bond.duration, bond.payment_frequency)
    for flow in flows:
        period+=1
        r+= present_value(flow.net_flow, period, coks)

    total_utility = utility(r,bond.commercial_value + (bond.flotation*bond.commercial_value)+(bond.cavali_cost*bond.commercial_value))
    
    result = Results(1, r, total_utility)

    return flows, result
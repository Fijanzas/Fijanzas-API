class Flow:
    def __init__(
        self,
        bond_id: int,
        period: int,
        initial_balance: float,
        amortization: float,
        coupon: float,
        bonus: float, # Prima redencion
        net_flow: float,
        final_balance: float,
    ):
        self.bond_id = bond_id
        self.period = period
        self.initial_balance = initial_balance
        self.amortization = amortization
        self.coupon = coupon
        self.bonus = bonus
        self.net_flow = net_flow
        self.final_balance = final_balance

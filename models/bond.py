class Bond:
    def __init__(
        self,
        user_id: int,
        nominal_value: float,
        commercial_value: float,
        coupon_rate: float, #TEA cupon
        market_rate: float, #TEA mercado
        payment_frequency: int,
        duration: int, #plazo
        bonus: float,
        flotation: float,
        cavali: float,
        structuration: float = 0.0,
        colocation: float = 0.0,
        total_grace_period: int = 0,
        partial_grace_period: int = 0,
    ):
        self.user_id = user_id
        self.nominal_value = nominal_value
        self.commercial_value = commercial_value
        self.coupon_rate = coupon_rate
        self.market_rate = market_rate
        self.payment_frequency = payment_frequency
        self.duration = duration
        self.bonus = bonus
        self.flotation = flotation
        self.cavali = cavali
        self.structuration = structuration
        self.colocation = colocation
        self.total_grace_period = total_grace_period
        self.partial_grace_period = partial_grace_period

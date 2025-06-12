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
        redemption_bonus: float,
        flotation: float,
        cavali_cost: float
    ):
        self.user_id = user_id
        self.nominal_value = nominal_value
        self.commercial_value = commercial_value
        self.coupon_rate = coupon_rate
        self.market_rate = market_rate
        self.payment_frequency = payment_frequency
        self.duration = duration
        self.redemption_bonus = redemption_bonus
        self.flotation = flotation
        self.cavali_cost = cavali_cost

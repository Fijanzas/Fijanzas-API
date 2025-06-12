class Results:
    def __init__(
            self,
            bond_id: int,
            theoretical_price: float,
            utility: float,
            ):
        self.bond_id = bond_id
        self.theoretical_price = theoretical_price
        self.utility = utility
        
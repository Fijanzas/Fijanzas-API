class Results:
    def __init__(
            self,
            results_id: int,
            bond_id: int,
            TCEA: float,
            TREA: float,
            Precio_Maximo: float,
            ):
        self.results_id = results_id
        self.bond_id = bond_id
        self.TCEA = TCEA
        self.TREA = TREA
        self.Precio_Maximo = Precio_Maximo
        
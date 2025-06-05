class Flujo:
    def __init__(
        self,
        id_bono: int,
        periodo: int,
        saldo_inicial: float,
        amortizacion: float,
        cupon: float,
        prima: float,
        flujo_neto: float,
        saldo_final: float,
    ):
        self.id_bono = id_bono
        self.periodo = periodo
        self.saldo_inicial = saldo_inicial
        self.amortizacion = amortizacion
        self.cupon = cupon
        self.prima = prima
        self.flujo_neto = flujo_neto
        self.saldo_final = saldo_final

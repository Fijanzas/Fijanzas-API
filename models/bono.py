class Bono:
    def __init__(
        self,
        valor_nominal: float,
        valor_comercial: float,
        tea_cupon: float,
        tea_mercado: float,
        frecuencia_pago: int,
        plazo_dias: int,
        prima_redencion: float,
        flotacion: float,
        costo_cavali: float,
        id_usuario: int
    ):
        self.valor_nominal = valor_nominal
        self.valor_comercial = valor_comercial
        self.tea_cupon = tea_cupon
        self.tea_mercado = tea_mercado
        self.frecuencia_pago = frecuencia_pago
        self.plazo_dias = plazo_dias
        self.prima_redencion = prima_redencion
        self.flotacion = flotacion
        self.costo_cavali = costo_cavali
        self.id_usuario = id_usuario
from models.flujo import Flujo
from models.bono import Bono
from models.resultados import Resultados

def amortizacion(valor_nominal, plazo_dias):
    return valor_nominal / plazo_dias 

def cupon_Periodo(valor_nominal, tea_cupon):
    return valor_nominal * tea_cupon

def cuota_periodo(valor_nominal, amortizacion, tea_cupon):
    return amortizacion + cupon_Periodo(valor_nominal, tea_cupon)

def prima_ultimo_flujo(porcentaje_prima, saldo_inicial_periodo, flujo):
    prima = porcentaje_prima * saldo_inicial_periodo
    return flujo + prima

def costos_iniciales(valor_comercial, flotacion, costo_cavali):
    return valor_comercial + (flotacion*valor_comercial) + (costo_cavali*valor_comercial)

def calcular_cok(tea_mercado, periodo, frecuencia_pago):
    return (1 + tea_mercado) ** (frecuencia_pago / periodo) - 1

def precio_presente(flujo, periodo, cok):
    return flujo / (1 + cok) ** periodo

def utilidad(precio, flujo_inicial):
    return precio - flujo_inicial

def metodo_aleman(bono):
    flujos = []
    saldo_inicial = bono.valor_nominal
    amortizacion_constante = amortizacion(bono.valor_nominal, bono.plazo_dias)

    for periodo in range(1, bono.plazo_dias + 1):
        cupon = cupon_Periodo(saldo_inicial, bono.tea_cupon)
        prima = 0.0
        if periodo == bono.plazo_dias:
            prima = bono.prima_redencion
            flujo_neto = prima_ultimo_flujo(prima, saldo_inicial, amortizacion_constante + cupon)
            saldo_final = 0.0
        else:
            flujo_neto = amortizacion_constante + cupon
            saldo_final = saldo_inicial - amortizacion_constante

        flujo = Flujo(
            id_bono=1,
            periodo=periodo,
            saldo_inicial=saldo_inicial,
            amortizacion=amortizacion_constante,
            cupon=cupon,
            prima=prima,
            flujo_neto=flujo_neto,
            saldo_final=saldo_final
        )
        flujos.append(flujo)
        saldo_inicial = saldo_final

    r=0
    periodo = 0
    coks = calcular_cok(bono.tea_mercado, bono.plazo_dias, bono.frecuencia_pago)
    for flujo in flujos:
        periodo+=1
        r+= precio_presente(flujo.flujo_neto, periodo, coks)

    utilidad_total = utilidad(r,bono.valor_comercial + (bono.flotacion*bono.valor_comercial)+(bono.costo_cavali*bono.valor_comercial))
    
    resultado =Resultados(1, r, utilidad_total)

    return flujos, resultado
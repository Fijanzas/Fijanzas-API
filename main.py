from models.flujo import Flujo
from models.bono import Bono
from models.resultados import Resultados
from metodoAleman import metodo_aleman

def main():
    bono = Bono(1000, 1050, 0.03923048454, 0.045, 2, 4, 0.01, 0.0045, 0.005, 1)

    flujos, resultado = metodo_aleman(bono)
    print("Flujos:")
    for flujo in flujos:
        print(vars(flujo))
    print("Resultado:")
    print(vars(resultado))


if __name__ == "__main__":
    main()
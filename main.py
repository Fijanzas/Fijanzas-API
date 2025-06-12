from models.bond import Bond
from metodoAleman import german_Amortization_Method

def main():
    bond = Bond(1, 1000, 1050, 0.03923048454, 0.045, 2, 4, 0.01, 0.0045, 0.005)

    flows, results = german_Amortization_Method(bond)
    print("Flujos:")
    for flow in flows:
        print(vars(flow))
    print("Resultado:")
    print(vars(results))


if __name__ == "__main__":
    main()
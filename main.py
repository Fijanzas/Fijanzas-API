from models.bond import Bond
from germanAmortizationMethod import german_Amortization_Method, TIR

def main():
            #  id  NV     CV     CR          MR   PF  D    B    F      CC    struct  col  TGP PGP  
    bond = Bond(1, 1200, 1200, 0.028635700, 0.002004008, 3, 6, 0.009, 0.0045, 0.005, 0.008, 0.009, 1, 1)

    flows,results = german_Amortization_Method(bond)
    print("Flujos:")
    for flow in flows:
        flow_dict = vars(flow)
        formatted_flow = {}
        for key, value in flow_dict.items():
            if isinstance(value, float):
                formatted_flow[key] = round(value, 2)
            else:
                formatted_flow[key] = value
        print(formatted_flow)
    print("\nResultados:")
    print("TCEA:", round(results.TCEA, 4))
    print("TREA:", round(results.TREA, 4))
    print("Precio Máximo:", round(results.Precio_Maximo, 2))



if __name__ == "__main__":
    main()
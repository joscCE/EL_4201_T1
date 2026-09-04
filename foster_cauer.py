import sympy as sp


def foster_to_cauer(R_values, C_values):

    s = sp.symbols('s')

    if len(R_values) != len(C_values):
        raise ValueError("Debe haber la misma cantidad de R y C.")

    #Construir Z(s) de Foster

    Z = 0

    for R, C in zip(R_values, C_values):
        R = sp.sympify(R)
        C = sp.sympify(C)

        Z += R / (1 + s * R * C)

    Z = sp.cancel(Z)

    print("\n================================")
    print(" IMPEDANCIA FOSTER")
    print("================================")
    print("Z(s) =")
    sp.pprint(Z)

    #Expansión Cauer
    
    elements = []
    current = Z

    for i in range(2 * len(R_values)):

        current = sp.cancel(current)

        # Si current -> infinito cuando s -> infinito,
        # extraemos un capacitor.
        degree_num = sp.degree(sp.numer(current), s)
        degree_den = sp.degree(sp.denom(current), s)

        if degree_num > degree_den:

            # C = coeficiente de s en la admitancia
            C = sp.limit(current / s, s, sp.oo)

            if C == 0:
                break

            elements.append(("C", sp.simplify(C)))

            # Restar s*C
            current = sp.cancel(current - s * C)

            # Invertir para obtener la siguiente impedancia
            current = sp.cancel(1 / current)

        else:

            # Extraemos resistencia
            R = sp.limit(current, s, sp.oo)

            if R == 0 or R is sp.oo:
                break

            elements.append(("R", sp.simplify(R)))

            # Restar R
            current = sp.cancel(current - R)

            # Invertir para obtener la siguiente admitancia
            current = sp.cancel(1 / current)

    #Mostrar resultados
    
    print("\n================================")
    print(" RED CAUER")
    print("================================")

    for i, (element, value) in enumerate(elements, 1):
        print(f"{element}{i} = ", end="")
        sp.pprint(value)

    return elements



#main
if __name__ == "__main__":

    R = []
    C = []

    foster_to_cauer(R, C)
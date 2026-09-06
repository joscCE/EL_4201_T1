import sympy as sp


def formato_resistencia(valor):
    """Devuelve una resistencia con una unidad práctica."""
    valor = float(sp.N(valor))
    unidades = [(1e9, "GΩ"), (1e6, "MΩ"), (1e3, "kΩ"), (1, "Ω"),
                (1e-3, "mΩ"), (1e-6, "µΩ")]

    for factor, unidad in unidades:
        if abs(valor) >= factor:
            return f"{valor / factor:.6g} {unidad}"
    return f"{valor:.6g} Ω"


def formato_capacitor(valor):
    """Devuelve un capacitor con una unidad práctica."""
    valor = float(sp.N(valor))
    unidades = [(1, "F"), (1e-3, "mF"), (1e-6, "µF"),
                (1e-9, "nF"), (1e-12, "pF")]

    for factor, unidad in unidades:
        if abs(valor) >= factor:
            return f"{valor / factor:.6g} {unidad}"
    return f"{valor:.6g} F"


def foster_to_cauer(R_values, C_values):
    s = sp.symbols('s')

    if len(R_values) != len(C_values):
        raise ValueError("Debe haber la misma cantidad de R y C.")

    # Construir Z(s) de Foster
    Z = 0
    for R, C in zip(R_values, C_values):
        R = sp.Rational(str(R))
        C = sp.Rational(str(C))
        Z += R / (1 + s * R * C)

    Z = sp.cancel(Z)

    print("\n================================")
    print(" IMPEDANCIA FOSTER")
    print("================================")
    print("Z(s) =")
    sp.pprint(Z)

    # Expansión Cauer
    # Alterna entre admitancia para extraer capacitores e impedancia
    # para extraer resistencias.
    elements = []
    current = Z
    state = "Z"

    for _ in range(2 * len(R_values)):
        current = sp.cancel(current)

        if state == "Z":
            if sp.limit(current, s, sp.oo) != 0:
                break
            current = sp.cancel(1 / current)
            state = "Y"

        C = sp.simplify(sp.limit(current / s, s, sp.oo))
        if C == 0 or not C.is_finite:
            break

        elements.append(("C", C))
        current = sp.cancel(current - s * C)
        current = sp.cancel(1 / current)
        state = "Z"

        R = sp.simplify(sp.limit(current, s, sp.oo))
        if R == 0 or not R.is_finite:
            break

        elements.append(("R", R))
        current = sp.cancel(current - R)
        current = sp.cancel(1 / current)
        state = "Y"

    # Mostrar resultados
    print("\n================================")
    print(" RED CAUER")
    print("================================")

    resistencias = []
    capacitores = []

    for i, (element, value) in enumerate(elements, 1):
        valor_numerico = float(sp.N(value))

        if element == "R":
            resistencias.append(valor_numerico)
            print(f"R{i} = {formato_resistencia(value)}")
        else:
            capacitores.append(valor_numerico)
            print(f"C{i} = {formato_capacitor(value)}")

    print("\n================================")
    print(" RESUMEN DE COMPONENTES")
    print("================================")

    print("\nResistencias:")
    for i, valor in enumerate(resistencias, 1):
        print(f"R{i} = {formato_resistencia(valor)}")

    print("\nCapacitores:")
    for i, valor in enumerate(capacitores, 1):
        print(f"C{i} = {formato_capacitor(valor)}")

    return elements


if __name__ == "__main__":
    R = [2.883625e-05, 0.0312931334640203, 0.0836443947170008, 0.194651492347688]
    C = [0.18049242898606752, 0.005534267691684129, 0.040015304991264024, 0.13897406477607008]

    foster_to_cauer(R, C)

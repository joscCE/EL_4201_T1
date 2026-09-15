import numpy as np

#PARÁMETROS DE ENTRADA 

V_GS = 12.0          # Voltaje de compuerta en encendido [V]
V_plateau = 5.8      # Voltaje de plateau [V]
R_G_ext = 35.0       # Resistencia externa de compuerta [Ohm]
R_G_int = 1.1        # Resistencia interna de compuerta del IRFP4868PbF [Ohm]
R_G = R_G_ext + R_G_int

# Parámetros del semiconductor (IRFP4868PbF)
t_ri = 50e-9         # Tiempo de subida 
t_fi = 45e-9         # Tiempo de caída de corriente 
Q_rr = 2520e-9       # Carga de recuperación inversa del diodo 

# Capacitancias de Miller C_rss obtenidas de la Fig. 5 
C_GD1 = 106e-12       # C_rss a V_DS ~ V_bus [F] 
C_GD2 = 2768e-12      # C_rss a V_DS ~ 0V [F] 

#DEFINICIÓN DE VECTORES PARA LA TABLA

v_ds_vec = np.array([150.0, 200.0, 250.0])   # Voltajes de bus DC [V]
i_d_vec = np.array([5.0, 10.0, 15.0, 20.0, 25.0])  # Corrientes I_D [A]

#CÁLCULO DE PÉRDIDAS DE CONMUTACIÓN

I_Gon = (V_GS - V_plateau) / R_G
I_Goff = V_plateau / R_G

# Matrices de salida para Eon y Eoff (en Joules)
E_on_matrix = np.zeros((len(v_ds_vec), len(i_d_vec)))
E_off_matrix = np.zeros((len(v_ds_vec), len(i_d_vec)))

for i, V_DD in enumerate(v_ds_vec):
    # Tiempos de caída y subida de voltaje (Efecto Miller)
    t_fu1 = (V_DD-1) * (C_GD1 / I_Gon)
    t_fu2 = (V_DD-1) * (C_GD2 / I_Gon)
    t_fu = (t_fu1 + t_fu2) / 2.0

    t_ru1 = (V_DD-1) * (C_GD1 / I_Goff)
    t_ru2 = (V_DD-1) * (C_GD2 / I_Goff)
    t_ru = (t_ru1 + t_ru2) / 2.0

    for j, I_D in enumerate(i_d_vec):
        # Eon: Transición de conmutación + Recuperación inversa
        E_on_matrix[i, j] = V_DD * I_D * ((t_ri + t_fu) / 2.0) + (Q_rr * V_DD)
        
        # Eoff: Transición de conmutación
        E_off_matrix[i, j] = V_DD * I_D * ((t_ru + t_fi) / 2.0)

#IMPRESIÓN DE RESULTADOS PARA PLECS
print("=== VECTORES DE CONFIGURACIÓN DE PLECS ===")
print(f"Vector V_DS [V]: {list(v_ds_vec)}")
print(f"Vector I_D [A] : {list(i_d_vec)}\n")

print("=== MATRIZ E_on [uJ] ===")
print(np.array2string(E_on_matrix * 1e6, precision=2, suppress_small=True))

print("\n=== MATRIZ E_off [uJ] ===")
print(np.array2string(E_off_matrix * 1e6, precision=2, suppress_small=True))

print("\n=== FORMATO LISTA DE MATLAB / PLECS (Eon en Joules) ===")
print(repr(E_on_matrix.tolist()))

print("\n=== FORMATO LISTA DE MATLAB / PLECS (Eoff en Joules) ===")
print(repr(E_off_matrix.tolist()))
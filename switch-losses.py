import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTES DEL CIRCUITO Y DRIVE ---
Rg = 35.0          # Resistencia de compuerta [Ohm]
Vplateau = 5.8     # Voltaje de plateau [V]
Vgs = 12.0         # Voltaje Gate-Source [V]
f_sw = 6e3         # Frecuencia de conmutación [Hz]

# Tiempos implícitos y carga de recuperación (ajustar si tienes datos de datasheet)
tri = 50e-9        # Tiempo de subida de corriente [s]
tfi = 45e-9        # Tiempo de caída de corriente [s]
Qrr = 2520e-9       # Carga de recuperación inversa [C]
Rds_on_25 = 32e-3   # RDS(on) a 25°C [Ohm]
Rds_on_175 = 0.31  # RDS(on) a 175°C [Ohm]

# --- DATOS DE CAPACITANCIA C_GD vs VDS ---
VDS_cap = np.array([1.0252, 1.4803, 2.9049, 3.4565, 4.5369, 6.9809])
C_cap   = np.array([2.7685e-09, 2.135e-09, 1.267e-09, 7.963e-10, 5.198e-10, 3.772e-10])

def get_cgd(vds_val):
    """Obtiene Cgd interpolando/extrapolando según el vector VDS_cap."""
    return np.interp(vds_val, VDS_cap, C_cap)

# --- DATOS DE PUNTOS DE OPERACIÓN ---
points = {
    25: {
        'VDS': [0.10556, 0.20394, 0.85532, 3.1911, 11.077, 32.689],
        'ID':  [1.9205, 3.1119, 4.6218, 6.0647, 6.4909, 8.1403],
        'Rds_on': Rds_on_25
    },
    175: {
        'VDS': [0.10377, 0.50453, 1.2858, 10.267, 18.421, 49.335],
        'ID':  [1.1659, 6.014, 15.815, 104.47, 121.42, 131.94],
        'Rds_on': Rds_on_175
    }
}

# --- CÁLCULO DE ENERGÍAS ---
for temp, data in points.items():
    print(f"\n==================== TEMPERATURA: {temp}°C ====================")
    rds = data['Rds_on']
    
    for vds, id_val in zip(data['VDS'], data['ID']):
        v_on = rds * id_val
        
        # Evaluaciones de Cgd en VDS_max y VDS_on
        cgd1 = get_cgd(vds)
        cgd2 = get_cgd(v_on)
        
        # 1. Tiempos de caída de voltaje en encendido (tfu)
        tfu1 = (vds - v_on) * Rg * (cgd1 / (Vgs - Vplateau))
        tfu2 = (vds - v_on) * Rg * (cgd2 / (Vgs - Vplateau))
        tfu = max(0.0, (tfu1 + tfu2) / 2.0)
        
        # 2. Tiempos de subida de voltaje en apagado (tru)
        tru1 = (vds - v_on) * Rg * (cgd1 / Vplateau)
        tru2 = (vds - v_on) * Rg * (cgd2 / Vplateau)
        tru = max(0.0, (tru1 + tru2) / 2.0)
        
        # 3. Energías [Julios]
        Eon = (vds * id_val * ((tri + tfu) / 2.0)) + (Qrr * vds)
        Eoff = vds * id_val * ((tru + tfi) / 2.0)
        
        # Salida formateada en microJulios (uJ) y Julios (J)
        print(f"Vds = {vds:7.3f} V | Id = {id_val:7.3f} A  ==>  "
              f"Eon = {Eon*1e6:9.2f} uJ ({Eon:.4e} J) | "
              f"Eoff = {Eoff*1e6:9.2f} uJ ({Eoff:.4e} J)")
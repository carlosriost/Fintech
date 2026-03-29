import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "edad": np.random.randint(18, 70, size=n),
    "ingreso_mensual": np.random.randint(800000, 8000000, size=n),
    "antiguedad_cuenta_meses": np.random.randint(1, 120, size=n),
    "num_transacciones_30d": np.random.randint(1, 200, size=n),
    "monto_promedio": np.random.randint(10000, 2000000, size=n),
    "dispositivo_nuevo": np.random.choice([0, 1], size=n, p=[0.8, 0.2]),
    "ip_compartida": np.random.choice([0, 1], size=n, p=[0.85, 0.15]),
    "hora_madrugada": np.random.choice([0, 1], size=n, p=[0.75, 0.25]),
})

# Regla simple para simular fraude
data["fraude"] = (
    (data["dispositivo_nuevo"] == 1) &
    (data["ip_compartida"] == 1) |
    (data["hora_madrugada"] == 1) &
    (data["monto_promedio"] > 1000000)
).astype(int)

data.to_csv("data/transacciones.csv", index=False)

print("Dataset generado en data/transacciones.csv")
print(data.head())
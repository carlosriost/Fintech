import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    "id_usuario": np.random.randint(1, 201, size=n),
    "edad": np.random.randint(18, 70, size=n),
    "ingreso_mensual": np.random.randint(800000, 8000000, size=n),
    "antiguedad_cuenta_meses": np.random.randint(1, 120, size=n),
    "num_transacciones_30d": np.random.randint(1, 200, size=n),
    "monto_promedio": np.random.randint(10000, 2000000, size=n),
    "dispositivo_nuevo": np.random.choice([0, 1], size=n, p=[0.8, 0.2]),
    "ip_compartida": np.random.choice([0, 1], size=n, p=[0.85, 0.15]),
    "hora_madrugada": np.random.choice([0, 1], size=n, p=[0.75, 0.25]),
    "dispositivo_id": np.random.randint(1, 120, size=n),
    "comercio_id": np.random.randint(1, 80, size=n)
})

# Crear IPs repetidas para simular riesgo
ips = [f"192.168.1.{i}" for i in np.random.randint(1, 60, size=n)]
df["ip"] = ips

# Regla simple de fraude
df["fraude"] = (
    ((df["dispositivo_nuevo"] == 1) & (df["ip_compartida"] == 1)) |
    ((df["hora_madrugada"] == 1) & (df["monto_promedio"] > 1000000))
).astype(int)

df.to_csv("data/transacciones_grafo.csv", index=False)

print("Archivo generado: data/transacciones_grafo.csv")
print(df.head())
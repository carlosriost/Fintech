import pandas as pd
import joblib
import time
import os
from datetime import datetime

# Archivo de entrada con datos
ARCHIVO_ENTRADA = "data/transacciones_grafo.csv"

# Archivo de salida para alertas
ARCHIVO_ALERTAS = "data/alertas_streaming.csv"

# Cargar modelo entrenado
modelo = joblib.load("models/modelo_fraude.pkl")

# Variables que el modelo espera
FEATURES_MODELO = [
    "edad",
    "ingreso_mensual",
    "antiguedad_cuenta_meses",
    "num_transacciones_30d",
    "monto_promedio",
    "dispositivo_nuevo",
    "ip_compartida",
    "hora_madrugada"
]

# Leer datos
df = pd.read_csv(ARCHIVO_ENTRADA)

# Si no existe el archivo de alertas, crearlo con encabezados
if not os.path.exists(ARCHIVO_ALERTAS):
    columnas_alerta = [
        "timestamp",
        "id_usuario",
        "ip",
        "dispositivo_id",
        "comercio_id",
        "monto_promedio",
        "fraude_predicho",
        "probabilidad_fraude"
    ]
    pd.DataFrame(columns=columnas_alerta).to_csv(ARCHIVO_ALERTAS, index=False)

print("Iniciando streaming simulado...\n")


for i, row in df.iterrows():
    # Preparar datos para el modelo
    datos_modelo = pd.DataFrame([row[FEATURES_MODELO]])

    # Predicción
    fraude_predicho = int(modelo.predict(datos_modelo)[0])
    probabilidad_fraude = float(modelo.predict_proba(datos_modelo)[0][1])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Transacción #{i+1}")
    print(f"Usuario: {row['id_usuario']} | IP: {row['ip']} | Dispositivo: {row['dispositivo_id']}")
    print(f"Monto promedio: {row['monto_promedio']}")
    print(f"Fraude predicho: {fraude_predicho} | Probabilidad: {probabilidad_fraude:.4f}")
    print("-" * 60)

    # Guardar alerta si parece sospechosa
    if fraude_predicho == 1 or probabilidad_fraude >= 0.80:
        alerta = pd.DataFrame([{
            "timestamp": timestamp,
            "id_usuario": int(row["id_usuario"]),
            "ip": row["ip"],
            "dispositivo_id": int(row["dispositivo_id"]),
            "comercio_id": int(row["comercio_id"]),
            "monto_promedio": int(row["monto_promedio"]),
            "fraude_predicho": fraude_predicho,
            "probabilidad_fraude": round(probabilidad_fraude, 4)
        }])

        alerta.to_csv(ARCHIVO_ALERTAS, mode="a", header=False, index=False)
        print("ALERTA: transacción sospechosa guardada en data/alertas_streaming.csv")
        print("=" * 60)

    # Esperar 2 segundos para simular llegada en tiempo real
    time.sleep(1)

print("\nStreaming finalizado.")
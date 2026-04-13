import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="API Principal - Detección de Fraude")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model-service:8001")
GRAPH_SERVICE_URL = os.getenv("GRAPH_SERVICE_URL", "http://graph-service:8002")

class TransaccionCompleta(BaseModel):
    id_usuario: int
    edad: int
    ingreso_mensual: int
    antiguedad_cuenta_meses: int
    num_transacciones_30d: int
    monto_promedio: int
    dispositivo_nuevo: int
    ip_compartida: int
    hora_madrugada: int
    dispositivo_id: int
    ip: str
    comercio_id: int

@app.get("/")
def servir_frontend():
    return FileResponse("frontend/index.html")

@app.post("/predecir")
def predecir(transaccion: TransaccionCompleta):
    model_payload = {
        "edad": transaccion.edad,
        "ingreso_mensual": transaccion.ingreso_mensual,
        "antiguedad_cuenta_meses": transaccion.antiguedad_cuenta_meses,
        "num_transacciones_30d": transaccion.num_transacciones_30d,
        "monto_promedio": transaccion.monto_promedio,
        "dispositivo_nuevo": transaccion.dispositivo_nuevo,
        "ip_compartida": transaccion.ip_compartida,
        "hora_madrugada": transaccion.hora_madrugada
    }

    graph_payload = {
        "id_usuario": transaccion.id_usuario,
        "ip": transaccion.ip,
        "dispositivo_id": transaccion.dispositivo_id
    }

    try:
        model_response = requests.post(
            f"{MODEL_SERVICE_URL}/predict",
            json=model_payload,
            timeout=10
        )
        model_response.raise_for_status()
        model_result = model_response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en model-service: {str(e)}")

    try:
        graph_response = requests.post(
            f"{GRAPH_SERVICE_URL}/riesgo-relacional",
            json=graph_payload,
            timeout=10
        )
        graph_response.raise_for_status()
        graph_result = graph_response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en graph-service: {str(e)}")

    riesgo_total = 1 if (
        model_result["fraude_predicho"] == 1
        or model_result["probabilidad_fraude"] >= 0.80
        or graph_result["riesgo_relacional"] == 1
    ) else 0

    return {
        "resultado_modelo": model_result,
        "resultado_grafo": graph_result,
        "riesgo_total": riesgo_total
    }
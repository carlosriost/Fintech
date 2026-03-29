from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Model Service - Fraude")

modelo = joblib.load("models/modelo_fraude.pkl")

class ModelInput(BaseModel):
    edad: int
    ingreso_mensual: int
    antiguedad_cuenta_meses: int
    num_transacciones_30d: int
    monto_promedio: int
    dispositivo_nuevo: int
    ip_compartida: int
    hora_madrugada: int

@app.get("/")
def inicio():
    return {"mensaje": "Model service funcionando"}

@app.post("/predict")
def predict(data: ModelInput):
    df = pd.DataFrame([data.model_dump()])
    prediccion = int(modelo.predict(df)[0])
    probabilidad = float(modelo.predict_proba(df)[0][1])

    return {
        "fraude_predicho": prediccion,
        "probabilidad_fraude": round(probabilidad, 4)
    }
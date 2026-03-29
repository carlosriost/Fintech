import pandas as pd
import joblib

df = pd.read_csv("data/transacciones.csv")
X = df.drop(columns=["fraude"])

modelo = joblib.load("models/modelo_fraude.pkl")

importancias = modelo.feature_importances_

resultado = pd.DataFrame({
    "variable": X.columns,
    "importancia": importancias
}).sort_values(by="importancia", ascending=False)

print(resultado)
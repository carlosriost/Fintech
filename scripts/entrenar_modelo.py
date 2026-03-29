import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Cargar datos
df = pd.read_csv("data/transacciones.csv")

# Variables de entrada
X = df.drop(columns=["fraude"])

# Variable objetivo
y = df["fraude"]

# Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Predicciones
y_pred = modelo.predict(X_test)

# Métricas
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}")
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Guardar modelo
joblib.dump(modelo, "models/modelo_fraude.pkl")
print("Modelo guardado en models/modelo_fraude.pkl")
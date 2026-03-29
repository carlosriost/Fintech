import os
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase

app = FastAPI(title="Graph Service - Neo4j")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

class GraphInput(BaseModel):
    id_usuario: int
    ip: str
    dispositivo_id: int

@app.get("/")
def inicio():
    return {"mensaje": "Graph service funcionando"}

@app.get("/health")
def health():
    try:
        driver.verify_connectivity()
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok").single()
            return {
                "estado": "ok",
                "servicio": "graph-service",
                "neo4j": "conectado",
                "resultado": result["ok"]
            }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Neo4j no responde: {str(e)}")

@app.post("/riesgo-relacional")
def riesgo_relacional(data: GraphInput):
    try:
        driver.verify_connectivity()

        with driver.session() as session:
            result_ip = session.run(
                """
                MATCH (u:Usuario)-[:SE_CONECTA_DESDE]->(ip:IP {direccion: $ip})
                RETURN count(DISTINCT u) AS total
                """,
                ip=data.ip
            ).single()

            result_dispositivo = session.run(
                """
                MATCH (u:Usuario)-[:USA]->(d:Dispositivo {dispositivo_id: $dispositivo_id})
                RETURN count(DISTINCT u) AS total
                """,
                dispositivo_id=data.dispositivo_id
            ).single()

            usuarios_misma_ip = result_ip["total"] if result_ip else 0
            usuarios_mismo_dispositivo = result_dispositivo["total"] if result_dispositivo else 0

            riesgo_relacional = 1 if usuarios_misma_ip > 1 or usuarios_mismo_dispositivo > 1 else 0

            return {
                "usuarios_misma_ip": usuarios_misma_ip,
                "usuarios_mismo_dispositivo": usuarios_mismo_dispositivo,
                "riesgo_relacional": riesgo_relacional
            }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno graph-service: {str(e)}")
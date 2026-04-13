import os
import pandas as pd
from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "12345678")

driver = GraphDatabase.driver(uri, auth=(user, password))

df = pd.read_csv("data/transacciones_grafo.csv")

def limpiar_base(tx):
    tx.run("MATCH (n) DETACH DELETE n")

def crear_grafo(tx, row):
    tx.run("""
        MERGE (u:Usuario {id_usuario: $id_usuario})
        SET u.edad = $edad,
            u.ingreso_mensual = $ingreso_mensual,
            u.antiguedad_cuenta_meses = $antiguedad_cuenta_meses

        MERGE (d:Dispositivo {dispositivo_id: $dispositivo_id})
        MERGE (ip:IP {direccion: $ip})
        MERGE (c:Comercio {comercio_id: $comercio_id})

        MERGE (u)-[:USA]->(d)
        MERGE (u)-[:SE_CONECTA_DESDE]->(ip)
        MERGE (u)-[:COMPRA_EN]->(c)
    """,
    id_usuario=int(row["id_usuario"]),
    edad=int(row["edad"]),
    ingreso_mensual=int(row["ingreso_mensual"]),
    antiguedad_cuenta_meses=int(row["antiguedad_cuenta_meses"]),
    dispositivo_id=int(row["dispositivo_id"]),
    ip=row["ip"],
    comercio_id=int(row["comercio_id"])
    )

with driver.session() as session:
    session.execute_write(limpiar_base)

    for _, row in df.iterrows():
        session.execute_write(crear_grafo, row)

driver.close()
print("Grafo cargado correctamente en Neo4j")
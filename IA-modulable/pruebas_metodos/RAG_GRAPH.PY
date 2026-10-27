# from llama_index import SimpleDirectoryReader
# documents = SimpleDirectoryReader("tus_pdfs/").load_data()

import os
from langchain_neo4j import Neo4jGraph

# Conectar a Neo4j con las credenciales locales
os.environ["NEO4J_URI"] = "bolt://localhost:7999"  # Puerto configurado en Docker
os.environ["NEO4J_USERNAME"] = "neo4j"            # Usuario configurado en Docker
os.environ["NEO4J_PASSWORD"] = "password"  # Tu contraseña

# Leemos las credenciales del entorno
neo4j_url      = os.environ["NEO4J_URI"]
neo4j_user     = os.environ["NEO4J_USERNAME"]
neo4j_password = os.environ["NEO4J_PASSWORD"]

# Crea la instancia
graph = Neo4jGraph(
    url=neo4j_url,
    username=neo4j_user,
    password=neo4j_password,
    database="neo4j"            # nombre de la BD (por defecto "neo4j")
)

results = graph.query("MATCH (p:Persona) RETURN p.nombre AS nombre, p.edad AS edad")
for rec in results:
    print(f"{rec['nombre']} → {rec['edad']} años")

# graph = Neo4jGraph(refresh_schema=False)
# print("Tipo de objeto:", type(graph))

# # Ver el esquema actual
# print("Esquema actual (posiblemente vacío):", graph.schema)

# # Refrescar esquema si lo necesitas
# graph.refresh_schema()
# print("Esquema después del refresh:", graph.schema)

# # Consulta Cypher de prueba
# result = graph.query("MATCH (n) RETURN n LIMIT 3")
# for r in result:
#     print(r)

# # Driver Neo4j de bajo nivel (más flexible)
# with graph._driver.session() as session:
#     res = session.run("MATCH (r) RETURN COUNT(r)")
#     print("Total de nodos:", res.single().value())























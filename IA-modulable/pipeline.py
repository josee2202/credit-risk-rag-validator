
import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG2 import RAG

def ejecutar_pipeline(path, nombre_coleccion):
    supervisor = RAG(path)
    docs = supervisor.load_documents()
    clean_docs = supervisor.clean(docs)
    base_chunks = supervisor.split(clean_docs, chunk_ss=800, chunk_so=200)
    supervisor.qdrant_record(base_chunks, collection_name=nombre_coleccion)


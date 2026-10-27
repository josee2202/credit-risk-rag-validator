import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG2 import RAG

# Flujo principal
if __name__ == "__main__":

# Documento de consulta
    query_path = r"<RAIZ_PROYECTO>\Bancos\<banco_A>\<documento_metodologico_A>.docx"
    consulta = RAG(query_path)
    query_docs = consulta.load_documents()
    query_chunks = consulta.split_query(query_docs, 600, 200)

    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")
    results = consulta.process_query_chunks_v2(query_chunks, collection_name="normativa")
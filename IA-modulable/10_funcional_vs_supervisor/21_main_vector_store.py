
import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG2 import RAG

path = r'<RAIZ_PROYECTO>\Contexto_Normativo\<carpeta_normativa_banco>'

# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional 
    normativa = RAG(path)

    # 1. - Leemos el documneto, en este caso es solo un word 
    normativa_cargada = normativa.load_documents()

    # 2. - Spliteamos 
    chunks = normativa.split(normativa_cargada, chunk_ss=800, chunk_so=100)

    # 3. - Almacenamos en nuestro Vectorstore 
    vector_store = normativa.qdrant_record(chunks, collection_name="normativa")
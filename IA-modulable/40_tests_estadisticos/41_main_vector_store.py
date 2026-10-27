import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG

path = r"<RAIZ_PROYECTO>\Contexto_Normativo\00. Contexto Normativo\TRIM CR Inspection tools - Methodological note to PD and LGD_(v1.1).pdf"

# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional 
    estadistico = RAG(path)

    # 1. - Leemos el documneto, en este caso es solo un word 
    tecnico_cargado = estadistico.read_document()

    # 2. - Spliteamos 
    chunks_funcional = estadistico.split(tecnico_cargado, chunk_ss=800, chunk_so=100)

    # 3. - Almacenamos en nuestro Vectorstore 
    vector_store = estadistico.faiss_method("estadistico_vdb")
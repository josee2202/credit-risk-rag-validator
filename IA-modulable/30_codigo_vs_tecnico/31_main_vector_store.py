import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG

path = r"<RAIZ_PROYECTO>\Bancos\<banco_B>\<documento_tecnico_B>.docx"

# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional 
    tecnico = RAG(path)

    # 1. - Leemos el documneto, en este caso es solo un word 
    tecnico_cargado = tecnico.read_document()

    # 2. - Spliteamos 
    chunks_funcional = tecnico.split(tecnico_cargado, chunk_ss=800, chunk_so=100)

    # 3. - Almacenamos en nuestro Vectorstore 
    vector_store = tecnico.faiss_method("tecnico_vdb")
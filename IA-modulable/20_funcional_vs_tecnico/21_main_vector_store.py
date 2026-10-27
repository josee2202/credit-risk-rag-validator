
import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG

path = '<RAIZ_PROYECTO>/Bancos/<banco_B>/<documento_metodologico_B>.docx'
# r'<RAIZ_PROYECTO>\Bancos\<banco_B>\<documento_metodologico_B>.docx'

# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional 
    funcional = RAG(path)

    # 1. - Leemos el documneto, en este caso es solo un word 
    funcional_cargado = funcional.read_document()

    # 2. - Spliteamos 
    chunks_funcional = funcional.split(funcional_cargado, chunk_ss=800, chunk_so=100)

    # 3. - Almacenamos en nuestro Vectorstore 
    vector_store = funcional.faiss_method("funcional_vdb")
import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG

path_query = r"<RAIZ_PROYECTO>\Bancos\<banco_B>\<documento_tecnico_B>.docx"

# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional
    tecnico_query = RAG(path_query)

    # 1. - Leemos el documneto, en este caso es solo un word 
    tecnico_cargado = tecnico_query.read_document()

    # 2. - Dividir la consulta en chunks
    query_chunks = tecnico_query.split_query(tecnico_cargado, 600, 200)
    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")

    # 3. - Cargamos los puntos almacenados en la base de datos 
    tecnico_query.load_vector_store("funcional_vdb")
    
    # Comparación 
    print("Procesando los chunks de la consulta...")
    resultados = tecnico_query.process_query_chunks_v2(query_chunks)

    # # Exportar resultados a Excel
    output_excel = r"<RAIZ_PROYECTO>\IA-modulable\Resultados\funcional_tecnico/contextos_recuperados_2.xlsx"
    tecnico_query.export_to_excel(resultados, output_excel)  

import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG

path_query = r"<RAIZ_PROYECTO>\IA-modulable\Resultados\procesos_sas\03_Traducción_generada\spliteado_con_macros\resultados_bloques_definitivo.docx"


# Flujo principal
if __name__ == "__main__":

    # Creamos instancia para el funcional
    traduccion_sas = RAG(path_query)

    # 1. - Leemos el documneto, en este caso es solo un word 
    sas_cargado = traduccion_sas.read_document()

    # 2. Dividir la consulta **solo** por el separador de líneas de '='
    pattern = r'(?m)^=+\s*$'
    query_chunks = traduccion_sas.split_query(
        query=sas_cargado,
        chunk_ss=None,            # desactiva el splitting recursivo
        chunk_so=None,
        separators=None,
        delimiter_pattern=pattern  # solo pre‐split por este patrón
    )
    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")


    # 3. - Cargamos los puntos almacenados en la base de datos 
    traduccion_sas.load_vector_store("tecnico_vdb")
    
    # Comparación 
    print("Procesando los chunks de la consulta...")
    resultados = traduccion_sas.process_query_chunks_v2(query_chunks)

    # 4. - Generar las respuestas para cada chunk
    print("Generando respuestas...")
    traduccion_sas.generar_respuesta()

    # 5. - Exportar resultados a Excel
    output_excel = r"<RAIZ_PROYECTO>\IA-modulable\Resultados\procesos_sas\05_respuestas_agente\respuestas.xlsx"
    traduccion_sas.export_to_excel(resultados, output_excel)  
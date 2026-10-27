import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG1 import RAG


if __name__ == "__main__":
    # Ruta del documento base
    path_directorio = r'<RAIZ_PROYECTO>\Contexto_Normativo\<carpeta_normativa_banco>'
    
    # Crear instancia de RAG para el documento base
    documento_base = RAG(path_directorio)
    
    # Leer el documento base
    doc_leido = documento_base.read_directory()
    print("Documento base leído correctamente.\n")
    
    # Dividir el documento en chunks
    doc_spliteado = documento_base.split(doc_leido, chunk_ss=800, chunk_so=100)
    
    # Crear vector store en memoria con los chunks generados
    vector_store = documento_base.faiss_method()

    # Ruta del documento de consulta
    path_query = r"<RAIZ_PROYECTO>\Bancos\<banco_A>\<documento_metodologico_A>.docx"
    
    # Crear instancia de RAG para el documento de consulta
    documento_consulta = RAG(path_query)
    
    query_procesada = documento_consulta.read_document(start_page=27, end_page=27)
    print("Documento de consulta leído correctamente.\n")
    
    # Dividir la consulta en chunks
    query_chunks = documento_consulta.split_query(query_procesada, 600, 200)
    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")
    
    # SOLUCIÓN: Usar el vector_store de documento_base para procesar la consulta
    print("Procesando los chunks de la consulta...")
    resultados = documento_consulta.process_query_chunks_v2(query_chunks)
    print(resultados)

    # # Exportar resultados a Excel
    # output_excel = r"<RAIZ_PROYECTO>\RESULTADOS\resultados_stop_words.xlsx"
    # documento_base.export_to_excel(resultados, output_excel)
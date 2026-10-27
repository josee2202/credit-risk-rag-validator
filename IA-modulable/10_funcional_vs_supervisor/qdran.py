import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from RAG3 import RAG

# Flujo principal
if __name__ == "__main__":
    # Directorio 
    path = '<RAIZ_PROYECTO>/Contexto_Normativo/00. Contexto Normativo/NIIF 9.diciembre 23.pdf'
    # Documento base
    # r"<RAIZ_PROYECTO>\Contexto_Normativo\<carpeta_normativa_banco>\Final Draft RTS on Assessment Methodology for IRB.pdf"
    supervisor = RAG(path)
    docs = supervisor.read_document()
    clean_docs = supervisor.clean(docs)
    base_chunks = supervisor.split(clean_docs, chunk_ss=800, chunk_so=200)
    supervisor.qdrant_record(base_chunks, collection_name="norma")

    # Documento de consulta
    query_path = '<RAIZ_PROYECTO>/Bancos/<banco_B>/<documento_metodologico_B>.docx'
    consulta = RAG(query_path, embeddings_func=supervisor.embeddings_func)
    query_docs = consulta.read_document()
    clean_docs = consulta.clean(docs)
    query_chunks = consulta.split_query(query_docs, 600, 200, sample_ratio=0.005)

    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")
    results = consulta.process_query_chunks_v2(query_chunks, collection_name="norma")

    consulta.generar_respuesta()

    # Exportar a excel
    from X_FUNCTIONS import export_to_excel

    output_path = 'resultado'
    export_to_excel(results, output_path, 'qdrant')
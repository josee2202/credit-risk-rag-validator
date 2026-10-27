
# * LIBRERIAS 
# * ==================================================================================================================
# pip install -qU langchain_community pypdf
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, Docx2txtLoader
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader     # Mantiene la estructura del documento y puede identificar elementos como títulos, listas, párrafos, o tablas.

from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


import numpy as np


# from langchain_community.vectorstores import Qdrant     # No uso langchain 

from langchain_community.vectorstores import FAISS
# import faiss

import os 

import logging

from config import config
cfg_param = config.cfg_param

from langchain_ollama import OllamaEmbeddings
ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
embed_model_name = cfg_param['llm']['embed']['name']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Cargar las variables de entorno del archivo .env
load_dotenv()


nomic_embedding_model = OllamaEmbeddings(
            base_url=ollama_endpoint,
            model=embed_model_name
        )

import spacy

from typing import List, Optional

from langchain_community.document_loaders import (DirectoryLoader, 
                                                  UnstructuredFileLoader) # deprecated in LangChain 0.2.8 and will be removed in 1.0.
# from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document

# Cargar spaCy (puedes mover esto al constructor si lo prefieres)
nlp = spacy.load("es_core_news_sm")

from X_qderant import QdrantHandler

# * FUNCIÓN RAG  
# * ==================================================================================================================

class RAG:
    def __init__(self, docPath, embeddings_func=nomic_embedding_model):
        self.path = docPath
        self.embeddings_func = embeddings_func  # Función de embedding (por ejemplo, OpenAIEmbeddings)
        self.texts = []  # Lista de textos para almacenar chunks
       
        self.results = None

        # Qdrant h self.vector_store = Noneandler
        self.qdrant = QdrantHandler(collection_name='prueba')
        

    # ! Preprocesamiento
    def load_documents(
        self,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None,
        recursive: bool = False,
        extension: Optional[str] = None,
    ) -> List[Document]:
        
        path = self.path

        # Directorio
        if os.path.isdir(path):
            print('Leyendo directorio')

            if extension:
                glob_pattern = f"**/*.{extension.lstrip('.')}"
            else:
                glob_pattern = "**/*"
            
            loader = DirectoryLoader(
                path=path,
                glob=glob_pattern,
                loader_cls=UnstructuredFileLoader,
                loader_kwargs={"mode": "single"},
                show_progress=True,
                recursive=recursive
            )
            docs = loader.load()
        # Fichero único
        else:
            print('Leyendo archivo individual')
            ext = os.path.splitext(path)[1].lower()
            loader = UnstructuredFileLoader(path, mode="single")
            docs = loader.load()
            if ext == ".pdf" and (start_page or end_page):
                total = len(docs)
                start = max(0, (start_page - 1) if start_page else 0)
                end = min(total, end_page) if end_page else total
                docs = docs[start:end]

        print('Extrayendo Metadatos (nombre de los archivos)')
        for doc in docs:
            src = doc.metadata.get("source", path)
            doc.metadata["filename"] = os.path.basename(src)

        return docs
    
    # * Limpieza  
    # * ===========================================================================
    def clean(self, docs):

        from X_FUNCTIONS import clean_text

        # Aseguramos que siempre trabajamos con una lista
        docs_list = docs if isinstance(docs, list) else [docs]

        for doc in docs_list:
            doc.page_content = clean_text(doc.page_content)

        # Opcional: devolver los docs (limpios) para poder encadenar llamadas
        return docs_list


    def split(self, texto, chunk_ss, chunk_so):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_ss,
            chunk_overlap=chunk_so
        )
        splits = text_splitter.split_documents(texto)
        self.texts = splits
        
        print(f'''Paso 2. - GENERACIÓN SPLITS - Se han generado {len(splits)} chunks''')
        return splits

    # * Qderant 
    # * ===========================================================================
    def qdrant_record(self, splits: List[Document], collection_name: str = None):
        # Delegar en el handler
        return self.qdrant.qdrant_record(splits, collection_name)
    
    def qdrant_retriever(self, query: str, k: int = 3, collection_name: str = None):
        return self.qdrant.qdrant_retriever(query, k, collection_name)

    # * Query 
    # * =========================================================================== 
    def split_query(self, query, chunk_ss, chunk_so, separators=None):
        """
        Devuelve chunks de la consulta, ya sea str o lista de Document.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_ss,
            chunk_overlap=chunk_so,
            separators=separators
        )
        if isinstance(query, str):
            docs = [Document(page_content=query)]
        elif isinstance(query, list) and all(hasattr(d, 'page_content') for d in query):
            docs = query
        else:
            raise TypeError("split_query espera str o lista de Document")
        return splitter.split_documents(docs)

    def process_query_chunks_v2(self, splits_query, collection_name: str = "document_embeddings"):
        """
        Procesa cada chunk de consulta y recupera contexto.
        """
        results = []
        print('Procesando cada chunk como query...')

        for i, chunk in enumerate(splits_query):
            text = chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
            print(f"Chunk {i+1}/{len(splits_query)}: {text[:50]}...")
            rel, ctx = self.qdrant_retriever(text, k=3, collection_name=collection_name)
            results.append({'chunk': text, 
                            'relevant_chunks': rel, 
                            'context': ctx})
        self.results = results
        
        return results

    def generar_respuesta(self):
            
        from X_AGENT import agente_text_model
            
        for result in self.results:
            # Llamada al Modelo para cada 'chunk' y su contexto
            answer = agente_text_model.get_answer(contexto=result['context'], pregunta=result['chunk'])
            
            # Asociar la respuesta al 'chunk' correspondiente
            result['respuesta'] = answer



# Flujo principal
if __name__ == "__main__":
    # Documento base
    base_path = '<RUTA_PDF_DE_PRUEBA>.pdf'
    # r"<RAIZ_PROYECTO>\Contexto_Normativo\<carpeta_normativa_banco>\Final Draft RTS on Assessment Methodology for IRB.pdf"
    supervisor = RAG(base_path)
    docs = supervisor.load_documents()
    clean_docs = supervisor.clean(docs)
    base_chunks = supervisor.split(clean_docs, chunk_ss=800, chunk_so=200)
    supervisor.qdrant_record(base_chunks, collection_name="prueba")

    # Documento de consulta
    query_path = r"<RAIZ_PROYECTO>\Bancos\<banco_A>\<documento_metodologico_A>.docx"
    consulta = RAG(query_path, embeddings_func=supervisor.embeddings_func)
    query_docs = consulta.load_documents()
    query_chunks = consulta.split_query(query_docs, 600, 200)

    print(f"Consulta dividida en {len(query_chunks)} chunks.\n")
    results = consulta.process_query_chunks_v2(query_chunks, collection_name="prueba")

    # Exportar a excel
    from X_FUNCTIONS import export_to_excel

    output_path = r'<RAIZ_PROYECTO>\IA-modulable\Resultados\00_Vector_store\Qderant'
    export_to_excel(results, output_path, 'qdrant')


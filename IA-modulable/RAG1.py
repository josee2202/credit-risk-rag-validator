
# * LIBRERIAS 
# * ==================================================================================================================
# pip install -qU langchain-community pypdf
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, Docx2txtLoader
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader     # Mantiene la estructura del documento y puede identificar elementos como títulos, listas, párrafos, o tablas.

from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

import numpy as np

from langchain_community.vectorstores import FAISS
# import faiss
from langchain_core.vectorstores import InMemoryVectorStore

import json
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
from langchain.document_loaders import AutoLoader, DirectoryLoader
from langchain_core.documents import Document

# Cargar spaCy (puedes mover esto al constructor si lo prefieres)
nlp = spacy.load("es_core_news_sm")

# * FUNCIÓN RAG  
# * ==================================================================================================================

class RAG:
    def __init__(self, docPath, embeddings_func=nomic_embedding_model):
        self.path = docPath
        self.embeddings_func = embeddings_func  # Función de embedding (por ejemplo, OpenAIEmbeddings)
        self.texts = []  # Lista de textos para almacenar chunks
        self.vector_store = None
        self.results = None

    # ! Preprocesamiento
    def read_document(self, start_page=None, end_page=None):
        if not os.path.isfile(self.path):
            raise FileNotFoundError("Archivo no encontrado o inaccesible.")

        if self.path.endswith(".pdf"):
            loader = PyPDFLoader(self.path, mode='page')
        elif self.path.endswith(".docx"):
            loader = Docx2txtLoader(self.path)
        else:
            raise ValueError("Formato de archivo no compatible. Use .pdf o .docx.")
        
        document = loader.load()

        if self.path.endswith(".pdf"):
            total_pages = len(document)
            print(f"El documento tiene {total_pages} páginas.")

            if start_page is not None and end_page is not None:
                if start_page < 1 or end_page > total_pages:
                    raise ValueError(f"Rango de páginas inválido. El documento tiene {total_pages} páginas.")
                selected_pages = document[start_page - 1:end_page]
            else:
                selected_pages = document

            return selected_pages  # Lista de Document

        else:
            from langchain_core.documents import Document    

            # Carga de .docx → un solo bloque
            print("Los documentos .docx no tienen páginas. Se procesará como un solo bloque.")
            full_text = document[0].page_content

            # Construimos el Document con metadata
            doc = Document(
                page_content=full_text,
                metadata={
                    "source": self.path,
                    "filename": os.path.basename(self.path)
                }
            )
            return [doc]
    
    def read_directory(self):
        loader = DirectoryLoader(
            path=self.path,
            glob="**/*.pdf",
            show_progress=True,
            loader_cls=PyPDFLoader,
            loader_kwargs={"mode": "single"}
        )
        docs = loader.load()
        
        # * Añadir 'filename' a los metadatos
        for doc in docs:
            source_path = doc.metadata.get("source", "")
            doc.metadata["filename"] = os.path.basename(source_path)

        print(f"Documentos cargados: {len(docs)}")
        return docs


    def split(self, texto, chunk_ss, chunk_so):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_ss,
            chunk_overlap=chunk_so
        )
        splits = text_splitter.split_documents(texto)
        self.texts = splits
        
        print(f'''Paso 2. - GENERACIÓN SPLITS - Se han generado {len(splits)} chunks''')
        return splits

    def faiss_method(self, carpeta_almacenar):
        print("Generando embeddings...")
        
        # Definimos la ruta final: ./embeddings/{carpeta_almacenar}/embeddings
        target_dir = f"./embeddings/{carpeta_almacenar}/embeddings"
        os.makedirs(target_dir, exist_ok=True)

        # Crear el vector store directamente con los documentos y sus metadatos
        self.vector_store = FAISS.from_documents(
            documents=self.texts,  # ahora contiene Document con metadatos
            embedding=self.embeddings_func
        )

        # Guardar en disco
        self.vector_store.save_local(target_dir)

        print("✅ Vector store creado exitosamente usando el método 'FAISS' con similitud coseno.")
        return self.vector_store
    
    def load_vector_store(self, carpeta_almacenar):
        """
        Carga desde ./embeddings/{carpeta_almacenar}/embeddings el FAISS index
        previamente guardado y lo asigna a self.vector_store.
        """
        path = f"./embeddings/{carpeta_almacenar}/embeddings"
        self.vector_store = FAISS.load_local(
            path,
            embeddings=self.embeddings_func,
            allow_dangerous_deserialization=True
        )
        print(f"✅ Vector store cargado desde {path}")
        return self.vector_store
    

    # ! INICIO DE LA QUERY 
    def split_query(self, query, chunk_ss=None, chunk_so=None, separators=None, delimiter_pattern=None):
        """
        Divide el texto de la query usando un patrón delimitador específico o el splitter recursivo.
        
        Args:
            query: Texto a dividir (str) o lista de Document
            chunk_ss: Tamaño de chunk para RecursiveCharacterTextSplitter
            chunk_so: Overlap de chunks
            separators: Lista personalizada de separadores para RecursiveCharacterTextSplitter
            delimiter_pattern: Patrón regex para dividir el texto antes de cualquier otro procesamiento
            
        Returns:
            Lista de objetos Document
        """
        from langchain_core.documents import Document
        import re
        
        # Convertir a lista de Document si es string
        if isinstance(query, str):
            # Si hay un patrón delimitador, dividir primero por ese patrón
            if delimiter_pattern:
                # Dividir por el patrón
                parts = re.split(delimiter_pattern, query)
                # Filtrar partes vacías y crear documents
                docs = [Document(page_content=part.strip()) for part in parts if part.strip()]
                print(f"Texto dividido en {len(docs)} partes usando el patrón delimitador")
            else:
                # No hay patrón, crear un solo documento
                docs = [Document(page_content=query)]
        elif isinstance(query, list) and all(hasattr(d, "page_content") for d in query):
            # Ya es una lista de Document
            docs = query
            
            # Si hay un patrón delimitador, aplicarlo a cada Document
            if delimiter_pattern:
                new_docs = []
                for doc in docs:
                    parts = re.split(delimiter_pattern, doc.page_content)
                    for part in parts:
                        if part.strip():
                            # Crear un nuevo documento pero conservar los metadatos originales
                            new_doc = Document(
                                page_content=part.strip(),
                                metadata=doc.metadata.copy() if hasattr(doc, "metadata") else {}
                            )
                            new_docs.append(new_doc)
                docs = new_docs
                print(f"Documents divididos en {len(docs)} partes usando el patrón delimitador")
        else:
            raise TypeError("split_query espera un str o una lista de Document.")
        
        # Si se especificó chunk_ss, aplicar el splitter recursivo después de la división por patrón
        if chunk_ss is not None:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_ss,
                chunk_overlap=chunk_so or 0,
                separators=separators
            )
            docs = splitter.split_documents(docs)
            print(f"Aplicado splitting recursivo: {len(docs)} chunks generados")
        
        self.texts = docs
        return docs


    # def split_query(self, query, chunk_ss, chunk_so, separators=None):
    #     """
    #     Devuelve una lista de Document como chunks, tanto si query
    #     es un string como si es una lista de Document.
    #     """

    #     splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=chunk_ss,
    #         chunk_overlap=chunk_so,
    #         separators=separators
    #     )

        # Si recibimos un string, lo transformamos en un único Document
        if isinstance(query, str):
            from langchain_core.documents import Document 
            docs = [Document(page_content=query)]
            return splitter.split_documents(docs)

        # Si recibimos lista de Document, lo pasamos directamente
        if isinstance(query, list) and all(hasattr(d, "page_content") for d in query):
            return splitter.split_documents(query)

        raise TypeError("split_query espera un str o una lista de Document.")

    def retriever(self, chunk: str, k: int = 3):
        # Recuperamos los Document originales
        docs = self.vector_store.similarity_search(chunk, k=k)
        
        # Sólo extraemos el texto de cada Document
        relevant_chunks = [doc.page_content for doc in docs]
        
        # Construimos el contexto combinado incluyendo filename y contenido
        combined_context = ""
        for doc in docs:
            filename = doc.metadata.get("filename", "desconocido")
            combined_context += (
                f"Documento: {filename} contiene esta información:\n"
                f"{doc.page_content}\n\n"
            )
            
        return relevant_chunks, combined_context


    def process_query_chunks_v2(self, splits_query):
        results = []

        print('Se va a iniciar un loop en el que cada chunk va a ser pasado como una query hasta generar la respuesta')

        for i, chunk in enumerate(splits_query):
            # Extraemos el texto ya sea de Document o de str
            if hasattr(chunk, "page_content"):
                text = chunk.page_content
            elif isinstance(chunk, str):
                text = chunk
            else:
                raise TypeError(f"Chunk de tipo no soportado: {type(chunk)}")

            print(f"\n--- Iteración {i}/{len(splits_query)} ---")
            print(f"Procesando chunk: {text[:50]}...")

            # Llamamos al retriever con el texto plano
            relevant_chunks, context = self.retriever(text, k=3)

            results.append({
                "chunk": text,
                "relevant_chunks": relevant_chunks,
                "context": context
            })

            self.results = results

        return results
    
    def generar_respuesta(self):
            
        from X_AGENT import agente_text_model
            
        for result in self.results:
            # Llamada al Modelo para cada 'chunk' y su contexto
            answer = agente_text_model.get_answer(contexto=result['context'], pregunta=result['chunk'])
            
            # Asociar la respuesta al 'chunk' correspondiente
            result['respuesta'] = answer


    def export_to_excel(self, results, output_path):
        """
        Exporta los resultados de búsqueda a un archivo Excel.
        
        Args:
            results (list): Lista de diccionarios con los resultados de búsqueda
            output_path (str): Ruta de salida para el archivo Excel
        
        Returns:
            str: Ruta del archivo Excel generado
        """
        import os
        import pandas as pd
        
        # Crear listas para las columnas del DataFrame
        chunks = []
        chunk_1 = []
        chunk_2 = []
        chunk_3 = []
        respuestas = []  # Lista para las respuestas
        
        # Extraer datos de los resultados
        for result in results:
            chunks.append(result["chunk"])
            
            # Asegurar que haya 3 chunks relevantes, o usar valores vacíos
            relevant_chunks = result["relevant_chunks"]
            chunk_1.append(relevant_chunks[0] if len(relevant_chunks) > 0 else "")
            chunk_2.append(relevant_chunks[1] if len(relevant_chunks) > 1 else "")
            chunk_3.append(relevant_chunks[2] if len(relevant_chunks) > 2 else "")
            
            # Agregar la respuesta generada para este chunk
            respuestas.append(result.get("respuesta", ""))  # Si no hay respuesta, añadir cadena vacía
        
        # Crear DataFrame con los nuevos resultados
        new_data = pd.DataFrame({
            "Query Chunk": chunks,
            "Chunk_1": chunk_1,
            "Chunk_2": chunk_2,
            "Chunk_3": chunk_3,
            "Respuesta": respuestas  # Añadir la columna 'Respuesta'
        })
        
        # Verificar si el archivo ya existe
        if os.path.exists(output_path):
            # Leer el archivo existente
            existing_data = pd.read_excel(output_path, engine='openpyxl')
            
            # Crear una fila vacía como separador
            separator_row = pd.DataFrame({
                "Query Chunk": [""],  # Fila vacía en la columna "Query Chunk"
                "Chunk_1": [""],      # Fila vacía en la columna "Chunk_1"
                "Chunk_2": [""],      # Fila vacía en la columna "Chunk_2"
                "Chunk_3": [""],      # Fila vacía en la columna "Chunk_3"
                "Respuesta": [""]     # Fila vacía en la columna "Respuesta"
            })
            
            # Concatenar los datos existentes, la fila vacía y los nuevos resultados
            combined_data = pd.concat([existing_data, separator_row, new_data], ignore_index=True)
        else:
            # Si no existe, usar solo los nuevos resultados
            combined_data = new_data
        
        # Exportar a Excel
        combined_data.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Resultados añadidos exitosamente a: {output_path}")
        return output_path




   
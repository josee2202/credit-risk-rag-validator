# Create a vector store with a sample text
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
import numpy as np

# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma  # Importa la clase necesaria

from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient


from config import config
cfg_param = config.cfg_param

from langchain_ollama import OllamaEmbeddings
ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
embed_model_name = cfg_param['llm']['embed']['name']

nomic_embedding_model = OllamaEmbeddings(
            base_url=ollama_endpoint,
            model=embed_model_name
        )



class VectorStore:
    def __init__(self, embeddings_func, texts):
        """
        Inicializa la clase VectorStore con un modelo de embeddings y una lista de textos.

        :param embeddings: Modelo de embeddings utilizado para generar vectores.
        :param texts: Lista de textos para generar vectores.
        """
        self.embeddings_func = embeddings_func
        self.texts = texts  # Guardar los textos en la instancia
        self.embedding_dim = None  # Dimensión del embedding (se calculará más tarde)
        
    def in_memory(self):
        """
        Crea un vector store en memoria utilizando los textos proporcionados en el constructor.

        :return: Instancia del vector store en memoria.
        """
        vector_store = InMemoryVectorStore.from_texts(
            texts=self.texts,
            embedding=self.embeddings_func
        )
        print("✅ Vector store creado exitosamente usando el método 'in_memory'.")

        return vector_store

    def facebook(self):
        """
        Crea un vector store utilizando FAISS con los textos proporcionados en el constructor.

        :return: Instancia del vector store FAISS.
        """
        # Generar los embeddings para los textos
        embeddings = self.embeddings_func.embed_documents(self.texts)

        # Determinar la dimensión del embedding (si no se ha calculado previamente)
        if self.embedding_dim is None:
            self.embedding_dim = len(embeddings[0])  # Dimensión del primer vector
        
        # Crear un índice FAISS
        index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Convertir los embeddings a un array numpy
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Agregar los embeddings al índice
        index.add(embeddings_array)
        
        # Crear un docstore para almacenar los documentos
        docstore = InMemoryDocstore({i: self.texts[i] for i in range(len(self.texts))})
        
        # Crear el mapeo entre índices y IDs del docstore
        index_to_docstore_id = {i: i for i in range(len(self.texts))}
        
        # Crear la instancia de FAISS
        vector_store = FAISS(
            embedding_function=self.embeddings_func,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id
        )
        
        print("✅ Vector store creado exitosamente usando el método 'facebook' (FAISS).")
        return vector_store

    def chroma(self, collection_name="chroma_collection", persist_directory="./chroma_langchain_db"):
        """
        Crea un vector store usando Chroma.

        :param collection_name: Nombre de la colección en Chroma.
        :param persist_directory: Directorio donde se guardarán los datos localmente.
        :return: Instancia del vector store de Chroma.
        """
        from langchain.vectorstores import Chroma  # Importa la clase necesaria

        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
        )
        print("✅ Vector store creado exitosamente usando el método 'chroma'.")

        return vector_store


    def mongodb(self, texts):
        """
        Crea un vector store usando MongoDB Atlas Vector Search.

        :param collection: Colección de MongoDB donde se almacenarán los vectores.
        :param index_name: Nombre del índice de búsqueda vectorial en MongoDB Atlas.
        :param relevance_score_fn: Función de puntuación de relevancia (por defecto: "cosine").
        :return: Instancia del vector store de MongoDB Atlas.
        """

        # Conexión a MongoDB
        mongo_client = MongoClient("mongodb://localhost:27017/")  # Conexión al contenedor de MongoDB
        db = mongo_client["mongo_database"]  # Nombre de la base de datos
        collection = db["vector_store_documents"]  # Nombre de la colección

        # Generar embeddings para los textos
        embeddings = self.embeddings.embed_documents(texts)

        # Insertar cada texto y su embedding en MongoDB
        try:
            for text, embedding in zip(texts, embeddings):
                collection.insert_one({
                    "text": text,               # Texto original
                    "embedding": embedding     # Embedding como una lista de números
                })
            print(f"✅ {len(texts)} documentos insertados correctamente en MongoDB.")
        except Exception as e:
            raise RuntimeError(f"Error al insertar datos en MongoDB: {e}")

        print("✅ Vector store creado exitosamente usando el método 'mongodb'.")
        return collection




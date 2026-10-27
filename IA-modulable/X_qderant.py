from typing import Optional, List
from qdrant_client import QdrantClient, models
from langchain_core.documents import Document
import numpy as np 

from config import config
cfg_param = config.cfg_param

from langchain_ollama import OllamaEmbeddings
# ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
# embed_model_name = cfg_param['llm']['embed']['name']

# nomic_embedding_model = OllamaEmbeddings(
#             base_url=ollama_endpoint,
#             model=embed_model_name
#         )


host = cfg_param['ollama']['host']
port = cfg_param['ollama']['port']
base_url = f"http://{host}:{port}"

embed_model_name = cfg_param['llm']['embed']['name']

nomic_embedding_model = OllamaEmbeddings(
    base_url=base_url,
    model=embed_model_name
)

class QdrantHandler:
    def __init__(self, embeddings_func = nomic_embedding_model, host: str = "localhost", port: int = 6333, collection_name: str = "document_embeddings"):
        """
        Handler para operaciones con Qdrant: inserción y recuperación de embeddings.
        """
        self.embeddings_func = embeddings_func
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

    def ensure_collection(self, vector_size: int):
        """
        Crea la colección en Qdrant si no existe.
        """
        existing = self.client.get_collections().collections
        names = [col.name for col in existing]
        if self.collection_name not in names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )

    def qdrant_record(self, splits: List[Document], collection_name: str = None):
        """
        Almacena embeddings y chunks en Qdrant solo si la colección está vacía.

        Args:
            splits (list[Document]): Lista de chunks de Document.
            collection_name (str): Nombre de la colección Qdrant. Si no se especifica, usa el por defecto.
        """
        try:
            name = collection_name or self.collection_name
            self.collection_name = name

            print(f"📦 Usando colección: {name}")
            print("🔍 Verificando existencia y contenido de la colección...")

            # Si la colección ya existe y tiene puntos, no hacemos nada
            collections = self.client.get_collections().collections
            existing = [col.name for col in collections]

            if name in existing:
                info = self.client.get_collection(collection_name=name)
                if info.points_count > 0:
                    print(f"✅ La colección '{name}' ya contiene {info.points_count} vectores. No se recalculan embeddings.")
                    return
                else:
                    print(f"⚠️ La colección '{name}' existe pero está vacía. Procediendo a generar embeddings...")
            else:
                print(f"🆕 La colección '{name}' no existe. Será creada.")

            # Generar embeddings
            print(f"🧠 Generando embeddings para {len(splits)} chunks...")
            texts = [chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in splits]
            embedding_matrix = np.array(self.embeddings_func.embed_documents(texts=texts))
            vector_size = embedding_matrix.shape[1]

            # Asegurar colección
            self.ensure_collection(vector_size)
            print(f"🛠️ Colección '{name}' lista para recibir vectores.")

            # Preparar puntos
            points = [
                models.PointStruct(
                    id=i,
                    vector=vector.tolist(),
                    payload={
                        "text": texts[i],
                        "filename": getattr(splits[i], 'metadata', {}).get('filename', None)
                    }
                ) for i, vector in enumerate(embedding_matrix)
            ]

            # Upsert por batches
            batch_size = 100
            print(f"📤 Subiendo {len(points)} vectores en lotes de {batch_size}...")
            for i in range(0, len(points), batch_size):
                self.client.upsert(collection_name=name, points=points[i:i + batch_size])

            print(f"✅ {len(points)} vectores almacenados en '{name}'.")

        except Exception as e:
            print(f"❌ Error al almacenar en Qdrant: {e}")




    def qdrant_retriever(self, query: str, k: int = 3, collection_name: str = None):
        """
        Recuperador usando Qdrant.

        Args:
            query (str): Texto de consulta.
            k (int): Número de resultados a recuperar.
            collection_name (str): Nombre de la colección Qdrant.

        Returns:
            relevant_chunks (list[str]), combined_context (str)
        """
        try:
            name = collection_name or self.collection_name
            # Embed query
            q_vec = self.embeddings_func.embed_query(query)
            # Asegurar colección vacía si no existe
            self.collection_name = name
            self.ensure_collection(len(q_vec))
            # Search
            results = self.client.search(
                collection_name=name,
                query_vector=q_vec,
                limit=k,
                with_payload=True,
                with_vectors=False
            )
            relevant_chunks, combined = [], []
            for pt in results:
                payload = pt.payload or {}
                text = payload.get('text', '')
                filename = payload.get('filename', 'desconocido')
                relevant_chunks.append(text)
                combined.append(f"Documento: {filename}\n{text}")
            return relevant_chunks, '\n\n'.join(combined)
        except Exception as e:
            print(f"Error en retriever de Qdrant: {e}")
            return [], ""   
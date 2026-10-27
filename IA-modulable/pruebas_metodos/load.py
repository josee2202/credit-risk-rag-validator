from langchain_community.vectorstores import FAISS

from config import config
cfg_param = config.cfg_param

from langchain_ollama import OllamaEmbeddings
ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
embed_model_name = cfg_param['llm']['embed']['name']

nomic_embedding_model = OllamaEmbeddings(
            base_url=ollama_endpoint,
            model=embed_model_name
        )




def retriever(chunk: str, k: int = 3):

    # Cargar vector store desde disco
    vector_store = FAISS.load_local(
        "./embeddings/embeddings",
        nomic_embedding_model,
        allow_dangerous_deserialization=True
    )
    relevant_chunks = vector_store.similarity_search(chunk, k=k)

    combined_context = ""
    for doc in relevant_chunks:
        filename = doc.metadata.get("filename", "desconocido")
        combined_context += f"Documento: {filename}\n{doc.page_content}\n\n"

    print(f"✅ Recuperados {len(relevant_chunks)} documentos relevantes.")
        
    return relevant_chunks, combined_context

results, contexto = retriever('Calculo de la Probabilidad de Default', 3)

print(contexto)


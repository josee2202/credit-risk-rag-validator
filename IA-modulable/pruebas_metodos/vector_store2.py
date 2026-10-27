

class VectorStore:
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
import nest_asyncio
import random
import time
import os
from dotenv import load_dotenv


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.core.evaluation import DatasetGenerator, FaithfulnessEvaluator, RelevancyEvaluator

# from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from langchain_ollama import OllamaEmbeddings
from llama_index.core.base.embeddings.base import BaseEmbedding

class LangchainOllamaEmbeddingAdapter(BaseEmbedding):
    def __init__(self, model: str):
        self.client = OllamaEmbeddings(model=model)

    def _get_text_embedding(self, text: str) -> list[float]:
        return self.client.embed_query(text)

    def _get_text_embedding_batch(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)

Settings.embed_model = LangchainOllamaEmbeddingAdapter(model="llama3")


from config import config
cfg_param = config.cfg_param

ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
llama32_1b_model_name = cfg_param['llm']['code']['name']
embed_model_name = cfg_param['llm']['embed']['name']

from llama_index.core.node_parser import SentenceSplitter


# Apply asyncio fix for Jupyter notebooks
nest_asyncio.apply()

# Utility functions
def evaluate_response_time_and_accuracy(chunk_size, eval_questions, eval_documents, faithfulness_evaluator,
                                        relevancy_evaluator):
    print(f"\n📏 Evaluando para chunk size: {chunk_size}")
    total_response_time = 0
    total_faithfulness = 0
    total_relevancy = 0

    print("🔧 Configurando modelo local para evaluación...")
    llm = Ollama(base_url=ollama_endpoint, model=llama32_1b_model_name, temperature=0, request_timeout=600)
    Settings.llm = llm

    Settings.embed_model = OllamaEmbeddings(base_url=ollama_endpoint, model=embed_model_name, temperature=0, request_timeout=600)

    print("🧩 Construyendo índice vectorial...")
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=min(50, chunk_size // 2))
    vector_index = VectorStoreIndex.from_documents(eval_documents, transformations=[splitter])
    query_engine = vector_index.as_query_engine(similarity_top_k=3)

    num_questions = len(eval_questions)
    print(f"📚 Procesando {num_questions} preguntas de evaluación...\n")

    for i, question in enumerate(eval_questions):
        print(f"🧠 [{i+1}/{num_questions}] Pregunta: {question}")
        start_time = time.time()
        response_vector = query_engine.query(question)
        elapsed_time = time.time() - start_time
        print(f"   ⏱ Tiempo de respuesta: {elapsed_time:.2f} segundos")

        faithfulness_result = faithfulness_evaluator.evaluate_response(response=response_vector).passing
        relevancy_result = relevancy_evaluator.evaluate_response(query=question, response=response_vector).passing
        print(f"   ✅ Faithfulness: {faithfulness_result}, 🎯 Relevancy: {relevancy_result}")

        total_response_time += elapsed_time
        total_faithfulness += faithfulness_result
        total_relevancy += relevancy_result

    average_response_time = total_response_time / num_questions
    average_faithfulness = total_faithfulness / num_questions
    average_relevancy = total_relevancy / num_questions

    print("\n📊 Resultados promedio:")
    print(f"   ⏱ Tiempo medio: {average_response_time:.2f}s")
    print(f"   ✅ Faithfulness: {average_faithfulness:.2f}")
    print(f"   🎯 Relevancy: {average_relevancy:.2f}\n")

    return average_response_time, average_faithfulness, average_relevancy


# Define the main class for the RAG method

class RAGEvaluator:
    def __init__(self, data_dir, num_eval_questions, chunk_sizes):
        print("🚀 Iniciando RAGEvaluator...")
        self.data_dir = data_dir
        self.num_eval_questions = num_eval_questions
        self.chunk_sizes = chunk_sizes

        print("📂 Cargando documentos...")
        self.documents = self.load_documents()

        print("🤖 Cargando modelo local...")
        self.llm_local = Ollama(base_url=ollama_endpoint, model=llama32_1b_model_name, temperature=0, request_timeout=600)

        print("❓ Generando preguntas de evaluación...")
        self.eval_questions = self.generate_eval_questions()

        print("🧪 Inicializando evaluadores...")
        self.faithfulness_evaluator = self.create_faithfulness_evaluator()
        self.relevancy_evaluator = self.create_relevancy_evaluator()

    def load_documents(self):
        return SimpleDirectoryReader(self.data_dir).load_data()

    def generate_eval_questions(self):
        eval_documents = self.documents[0:5]
        data_generator = DatasetGenerator.from_documents(eval_documents, llm=self.llm_local)
        eval_questions = data_generator.generate_questions_from_nodes()
        print(f"✅ Generadas {len(eval_questions)} preguntas.")
        return random.sample(eval_questions, self.num_eval_questions)

    def create_faithfulness_evaluator(self):
        print("🔍 Configurando evaluador de *faithfulness*...")
        faithfulness_evaluator = FaithfulnessEvaluator(llm=self.llm_local)
        faithfulness_new_prompt_template = PromptTemplate("""Please tell if a given piece of information is directly supported by the context.
You need to answer with either YES or NO.
Answer YES if any part of the context explicitly supports the information, even if most of the context is unrelated. If the context does not explicitly support the information, answer NO.
...""")
        faithfulness_evaluator.update_prompts({"your_prompt_key": faithfulness_new_prompt_template})
        return faithfulness_evaluator

    def create_relevancy_evaluator(self):
        print("🔍 Configurando evaluador de *relevancy*...")
        return RelevancyEvaluator(llm=self.llm_local)

    def run(self):
        print("\n🏃 Ejecutando evaluación de RAG...\n")
        for chunk_size in self.chunk_sizes:
            evaluate_response_time_and_accuracy(
                chunk_size,
                self.eval_questions,
                self.documents[0:20],
                self.faithfulness_evaluator,
                self.relevancy_evaluator
            )


# Argument Parsing
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='RAG Method Evaluation')
    parser.add_argument('--data_dir', type=str, default='../data', help='Directory of the documents')
    parser.add_argument('--num_eval_questions', type=int, default=5, help='Number of evaluation questions')
    parser.add_argument('--chunk_sizes', nargs='+', type=int, default=[128, 256], help='List of chunk sizes')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print("📌 Argumentos recibidos:")
    print(f"   📁 Carpeta: {args.data_dir}")
    print(f"   ❓ Preguntas: {args.num_eval_questions}")
    print(f"   🧩 Chunk sizes: {args.chunk_sizes}\n")

    evaluator = RAGEvaluator(
        data_dir=args.data_dir,
        num_eval_questions=args.num_eval_questions,
        chunk_sizes=args.chunk_sizes
    )
    evaluator.run()
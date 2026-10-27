from datasets import Dataset
from ragas.metrics import ContextRelevance
from ragas import evaluate

from config import config
from langchain_ollama.llms import OllamaLLM
from ragas.llms import LangchainLLMWrapper

import pandas as pd


# config parameters
cfg_param = config.cfg_param

ollama_endpoint = f"{cfg_param['ollama']['host']}:{cfg_param['ollama']['port']}"
embed_model_name = cfg_param['llm']['embed']['name']
text_model_name = cfg_param['llm']['text']['name']

# Agente 
class Agente:
    def __init__(self, ollama_endpoint, model_name, temperature = 0):
        self.llm = OllamaLLM(base_url=ollama_endpoint, model=model_name, temperature = temperature)
        
llm_eval = Agente(ollama_endpoint, text_model_name)
llm_wrapper = LangchainLLMWrapper(llm_eval.llm)


# ! Pruebas con el excel 

# Cargar Excel
df = pd.read_excel(r"<RAIZ_PROYECTO>\RESULTADOS\resultados_splitter_no_sep.xlsx")  


# Detectar columnas de chunks
chunk_cols = [col for col in df.columns if col.startswith("Chunk_")]

# Tomar solo la primera fila no vacía
primer_caso = df[df["Query Chunk"].notnull()].iloc[0:1].copy()

# Limpiar saltos de línea por seguridad
primer_caso[["Query Chunk"] + chunk_cols] = (
    primer_caso[["Query Chunk"] + chunk_cols]
    .fillna("")
    .astype(str)
    .replace(r"[\r\n]+", " ", regex=True)
)

# Crear dataset para RAGAS
data = Dataset.from_dict({
    "question": primer_caso["Query Chunk"].tolist(),
    "retrieved_contexts": primer_caso[chunk_cols].values.tolist(),
    "answer": [""]  # debe tener el mismo largo
})

# Evaluar usando ContextRelevance
context_relevance = ContextRelevance()
result = evaluate(data, metrics=[context_relevance], llm=llm_wrapper)

# Mostrar resultado
print(result.to_pandas())






# Identificar bloques usando filas vacías como separadores
# df["is_empty"] = df["Query Chunk"].isnull()
# df["block_id"] = df["is_empty"].cumsum()
# df = df[~df["is_empty"]].drop(columns="is_empty")
# resultados = []

# import asyncio

# async def evaluar_bloque(data, llm_wrapper, context_relevance):
#     result = await evaluate(
#         data,
#         metrics=[context_relevance],
#         llm=llm_wrapper,
#         # concurrency_level=2
#     )
#     return result

# for block_id, block_df in df.groupby("block_id"):
#     print(f"🧪 Evaluando bloque {block_id} con {len(block_df)} filas")
#     block_df = block_df.copy()

#     for col in ["Query Chunk"] + chunk_cols:
#         block_df[col] = block_df[col].fillna("").astype(str).str.replace(r"[\r\n]+", " ", regex=True)

#     data = Dataset.from_dict({
#         "question": block_df["Query Chunk"].tolist(),
#         "retrieved_contexts": block_df[chunk_cols].values.tolist(),
#         "answer": [""] * len(block_df)
#     })

#     result = asyncio.run(evaluar_bloque(data, llm_wrapper, context_relevance))
#     block_df["ContextRelevance"] = result["context_relevance"]
#     resultados.append(block_df)

# print(resultados)





# Dataset con la columna correcta
# data = Dataset.from_dict({
#     "question": [
#         "El Congreso podrá dictar normas sobre contratación estatal..."
#     ],
#     "retrieved_contexts": [[
#         "La contratación estatal se regirá por los principios de transparencia...",
#         "La ley determinará los contratos a los que no se aplican estas normas..."
#     ]],
#     "answer": [""]
# }) 

# # Evaluar
# results = evaluate(data, metrics=[context_relevance], llm=llm_wrapper)
# print(results)
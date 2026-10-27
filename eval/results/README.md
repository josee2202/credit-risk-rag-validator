# Resultados de la evaluación

Generado por `eval/run_eval.py`. Corpus sintético (ver `examples/synthetic_corpus.py`): 10 secciones de un
documento metodológico ficticio, 8 con un requisito aplicable en la guía sintética (5 alineadas y 3 con
desviaciones deliberadas) y 2 sin requisito aplicable. Embeddings `nomic-embed-text` (Ollama), Qdrant, top-3.

## Recuperación (M1-M8)

| Colección de referencia | Fragmentos | Hit@1 | Hit@3 | MRR@3 | Indexación |
|---|---:|---:|---:|---:|---:|
| guia_sintetica | 6 | 1.00 | 1.00 | 1.00 | 2 s |
| guia_sintetica+anejo9_boe | 355 | 0.88 | 0.88 | 0.88 | 99 s |

## Similitud del mejor fragmento: secciones con y sin requisito aplicable

| Colección | Con requisito (M1-M8): mín - máx | Sin requisito (M9, M10) |
|---|---|---|
| guia_sintetica | 0.713 - 0.835 | 0.683, 0.661 |
| guia_sintetica+anejo9_boe | 0.731 - 0.835 | 0.683, 0.721 |

## Veredicto del LLM (M1-M10, contexto recuperado de la guía sintética)

Cada respuesta se clasifica de dos formas: una heurística de palabras clave fijada antes de ver los
resultados y una revisión manual de la respuesta completa (`revision_manual.json`, con justificación).
La revisión manual es la referencia; la tabla muestra también dónde discrepan.

| Modelo | Aciertos (manual) | Aciertos (heurística) | Dice "alineado" en los 5 casos no alineados o sin requisito | Segundos/respuesta (CPU) |
|---|---:|---:|---:|---:|
| llama3.2:1b | 5/10 | 5/10 | 5/5 | 55.2 |
| llama3.2:3b | 6/10 | 5/10 | 2/5 | 55.3 |

| Sección | Esperado | llama3.2:1b (heur.) | llama3.2:1b (manual) | llama3.2:3b (heur.) | llama3.2:3b (manual) |
|---|---|---|---|---|---|
| M1 Definición de default | alineado | alineado | alineado | alineado | alineado |
| M2 Muestra de desarrollo | no_alineado | alineado | alineado | alineado | no_alineado |
| M3 Ciclo económico y conservadurismo | no_alineado | alineado | alineado | alineado | ambiguo |
| M4 Calibración | alineado | alineado | alineado | alineado | alineado |
| M5 Poder discriminante | alineado | alineado | alineado | alineado | alineado |
| M6 Escenarios prospectivos | no_alineado | alineado | alineado | alineado | alineado |
| M7 Calidad de los datos | alineado | alineado | alineado | alineado | alineado |
| M8 Ajustes manuales | alineado | alineado | alineado | alineado | alineado |
| M9 Organización del equipo | sin_evidencia | alineado | alineado | no_alineado | no_alineado |
| M10 Formato del documento | sin_evidencia | alineado | alineado | alineado | alineado |

Las respuestas completas están en `llm_<modelo>.json`. El modelo de 1B a menudo repite la plantilla
del prompt antes de responder.

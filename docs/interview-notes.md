# Notas para entrevistas

Documento de preparación personal. Las cifras proceden de `eval/results/README.md` y de las
ejecuciones descritas en el README. No hay métricas de negocio ni usuarios reales.

## 1. El proyecto en 60–90 segundos

> En validación de modelos de riesgo de crédito hay que comprobar que la documentación de un modelo
> de PD es coherente con la normativa y con su propia implementación. Hoy eso se hace leyendo a mano
> documentos de cien páginas y código SAS.
>
> Construí, como TFM, un sistema RAG totalmente local que lo hace fragmento a fragmento. Indexa la
> referencia en Qdrant con embeddings de `nomic-embed-text` servidos por Ollama, usa cada párrafo del
> documento revisado como consulta y devuelve los tres pasajes más parecidos con fichero, página y
> similitud. Opcionalmente, un Llama 3.2 local emite un veredicto. Tiene cuatro modos, uno de ellos
> traduce código SAS a lenguaje natural antes de compararlo, y se usa desde FastAPI y Streamlit.
>
> Al retomarlo en 2026, con ayuda de un asistente de IA, lo estabilicé y lo medí. Con un corpus
> etiquetado y la Circular 4/2017 real como distractor, la recuperación encuentra el requisito correcto
> entre los tres primeros en 7 de 8 casos. Pero el modelo de 1B dice "alineado" a las 10 secciones,
> también a las tres desviaciones introducidas a propósito.
> La conclusión es que el sistema sirve como buscador de evidencias trazables, no como juez
> automático. Eso orienta el siguiente paso: veredictos estructurados, umbral de "sin evidencia" y
> un modelo mayor.

## 2. Tres decisiones técnicas y sus alternativas

1. **Stack 100 % local (Ollama + Qdrant) frente a APIs gestionadas.** La documentación de modelos de
   un banco es confidencial. Lo local evita que salga de la máquina y no tiene coste por token. A
   cambio, la latencia en CPU es alta (unos 0,3 s por fragmento al indexar y ~55 s por
   veredicto) y los modelos pequeños razonan mal. Con APIs (OpenAI) o un vector store gestionado
   habría más calidad, pero haría falta un acuerdo de tratamiento de datos.
2. **Cada fragmento del documento revisado es una consulta.** Frente al RAG clásico de preguntas y
   respuestas, garantiza cobertura: ningún párrafo se queda sin revisar. El coste es lineal con la
   longitud del documento; por eso existe `doc_sample_ratio`, que hoy toma el primer X %, no una
   muestra aleatoria.
3. **SAS → texto → comparación texto-texto.** El código se trocea por macros (`%macro … %mend`), se
   agrupa bajo un presupuesto de tokens medido con un tokenizador SentencePiece y el LLM lo explica
   con un resumen acumulado de los bloques previos. Alternativas: hacer embeddings del código tal
   cual, que alinea mal con la prosa de los documentos técnicos, o analizar el SAS sintácticamente,
   que es más preciso pero mucho más costoso de construir.

## 3. Dificultades y cómo se resolvieron

Las de la recuperación de octubre de 2026 están verificadas con tests que fallan si se reintroduce
cada fallo.

- **Dependencias no instalables.** El `requirements.txt` fijaba `numpy==1.26.4` junto a
  `thinc==8.3.6`, que exige `numpy>=2`. La carga de spaCy en el flujo principal no se usaba, así que
  se eliminó y se fijó un lock con las mismas versiones originales.
- **Ollama rechazaba lotes grandes de embeddings.** Con ~250 textos o más fallaba `/tokenize:
  connection reset`, y un PDF de 349 fragmentos no se indexaba. Se aisló midiendo por tamaño de lote
  (128 era estable y 256 fallaba de forma intermitente) y se pasó a lotes de 32.
- **Generación desbocada del LLM con SAS real.** Con un programa SAS real de 510 líneas, la primera
  llamada no terminaba: los logs de Ollama mostraban 38.000 tokens generados en 2 h por una sola
  petición, con temperatura 0 el modelo de 1B había entrado en bucle. Se añadió un límite de salida
  configurable (`num_predict`, `LLM_MAX_TOKENS`, 1.024 por defecto) con su test. Al repetirlo, el flujo
  completo tardó 468 s y la llamada problemática se cortó en el límite. La lección: en una herramienta
  local cada llamada al modelo necesita un límite explícito.
- **Fallos silenciosos.** El manejador de Qdrant imprimía el error y seguía, así que la API respondía
  200 con cero evidencias. Ahora los errores se propagan: 400 para entradas no válidas y 500 con la
  causa.
- **Errores funcionales:**
  - la UI dejaba subir varios documentos de referencia, pero solo se indexaba el primero;
  - un `.sas` en "Código vs Estadístico" daba error;
  - "Funcional vs Técnico" usaba el prompt de revisión de código;
  - el prompt normativo tenía invertidos los papeles de norma y documento del banco;
  - la tabla de la UI fallaba con menos de 3 evidencias.
- **Evaluación honesta.** La primera métrica de recuperación estaba mal: etiquetaba cada fragmento
  con un solo requisito cuando contiene 2–3, y daba Hit@1 = Hit@3 = 0,62 con solo 6 fragmentos. Se
  detectó porque el número era inverosímil y se redefinió por contención (≥60 % de las palabras del
  requisito): 8/8 y 7/8. Los veredictos del LLM se revisaron a mano además de con la heurística,
  que discrepaba en 2 de 20 respuestas.

## 4. Resultados verificables y limitaciones

- Recuperación: Hit@3 de 8/8 solo con la guía sintética y de 7/8 con el Anejo 9 real como
  distractor (MRR@3 de 1,00 y 0,88). El fallo es la sección de ajustes manuales.
- Sin evidencia: la similitud del mejor fragmento separa las secciones sin requisito por solo 0,01,
  así que un umbral fijo no sería fiable.
- Veredictos, revisados uno a uno: 5/10 con `llama3.2:1b`, que dice "alineado" a las 10 secciones, y
  6/10 con `llama3.2:3b`, que detecta "3 años frente a ≥5" pero da por buena la desviación de
  escenario único.
- Comprobado a escala real en local con documentos privados (solo cifras agregadas):
  - un documento metodológico de ~20.000 palabras: 295 fragmentos validados contra 349 fragmentos
    del Anejo 9 en 169 s sin LLM (indexación incluida) y una muestra del 5 % con LLM, unos 40 s por
    fragmento;
  - un SAS real de 510 líneas: 5 grupos traducidos y validados contra un documento técnico real en
    468 s, tras la corrección del bucle.
- Hay 20 tests y una CI que ejecuta la demo con embeddings reales.
- Limitaciones:
  - corpus de evaluación pequeño y sintético;
  - sin umbral de "sin evidencia";
  - muestreo no aleatorio;
  - reutilización silenciosa de colecciones con el mismo nombre;
  - pensado para un solo usuario.

## 5. Qué cambiaría para un uso real a mayor escala

- **Veredicto estructurado** (JSON con etiqueta y cita literal), umbral de similitud y etiqueta "no
  aplicable". Evaluado con un conjunto anotado por validadores.
- **Modelo mayor**, en GPU local o en un endpoint privado con acuerdo de datos, y prefijos de tarea
  de `nomic-embed-text`. Tras medirlos, quizá *reranking* con un cross-encoder.
- **Colecciones versionadas** por hash del documento y metadatos de versión de la norma.
- **Ingesta asíncrona** con una cola de trabajos, endpoint no bloqueante, autenticación y control
  de acceso por documento.
- **OCR** para PDFs escaneados y troceado por estructura (títulos y artículos) en lugar de por
  caracteres.

## 6. Preguntas previsibles

**¿Cómo evitas que el LLM alucine?** No lo evito del todo. Los prompts piden responder solo con el
contexto (`prompt.py`) y la temperatura es 0, pero la evaluación muestra que el modelo de 1B afirma
alineación sin base. Por eso la salida principal son las evidencias con fuente, página y similitud,
y el veredicto es una pista. El siguiente paso es un veredicto estructurado con cita obligatoria y
una etiqueta "no aplicable".

**¿Por qué Qdrant y no FAISS?** En el desarrollo se probaron FAISS y un vector store en memoria
(`RAG1.py`, `pruebas_metodos/`). Qdrant aporta colecciones con nombre persistentes, que permiten
indexar una norma una vez y reutilizarla, además de payloads con fuente y página. Puede ejecutarse
como servidor o embebido (`QDRANT_LOCATION=./qdrant_storage`); los tests lo usan en memoria.

**¿Cómo mediste la calidad de la recuperación?** `eval/run_eval.py`: 10 secciones etiquetadas de un
documento ficticio como consultas y top-3 por similitud coseno. Un fragmento es relevante si
contiene ≥60 % de las palabras del requisito etiquetado. Calculo Hit@1, Hit@3 y MRR, con y sin
350 fragmentos de la Circular 4/2017 real como distractores. Además comparo la similitud del mejor
fragmento en secciones sin requisito aplicable para ver si un umbral serviría.

**¿Cómo tratas el código SAS largo?** `Codigo_sas.py` separa macros completas con una expresión
regular, agrupa bloques hasta un presupuesto de tokens (2.400 menos el prompt y un margen), divide
los bloques que no caben y genera una explicación por grupo. Cada explicación se resume y se pasa
como contexto al siguiente grupo. Limitación: ese resumen acumulado crece y puede superar la
ventana de contexto en programas largos.

**¿Qué pasa si Ollama o Qdrant no están disponibles?** Antes la API devolvía 200 con resultados
vacíos, que era el peor caso para una herramienta de control. Ahora el error se propaga y la API
responde 500 con la causa, y la UI la muestra. Hay tests que simulan la caída de Ollama.

## Qué existía y qué aportó la recuperación

La recuperación se hizo con ayuda de un asistente de IA (Claude Code), como reflejan los commits
(`Co-Authored-By`). Conviene decirlo si sale el tema y poder explicar cada cambio: están separados en
commits pequeños y las correcciones funcionales tienen su test. La revisión manual de los 20 veredictos
(`eval/results/revision_manual.json`) también la hizo el asistente: repásala tú antes de citar esas cifras.

- **Existía (TFM, 2025):**
  - el pipeline RAG (`RAG3.py`, `X_qderant.py`);
  - la API FastAPI y la UI Streamlit;
  - el procesamiento de SAS y los prompts;
  - los cuatro modos de validación;
  - los experimentos con FAISS y en memoria, limpieza de texto, *stop words* y RAGAS.
- **Recuperación (octubre de 2026):**
  - correcciones de dependencias, embeddings por lotes, propagación de errores y configuración;
  - referencias múltiples, SAS en todos los modos, prompts y UI;
  - fuente, página y similitud en los resultados;
  - el límite de tokens del LLM;
  - los 20 tests, el corpus sintético, la demo, la evaluación, la CI y la documentación.

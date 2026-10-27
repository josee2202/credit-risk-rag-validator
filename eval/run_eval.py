"""Evaluación pequeña y reproducible del pipeline (recuperación + veredicto del LLM).

Requiere Ollama y Qdrant en marcha y el Anejo 9 descargado:

    python examples/public/download_anejo9.py
    python eval/run_eval.py                          # recuperación + veredictos con llama3.2:1b
    python eval/run_eval.py --modelos llama3.2:1b llama3.2:3b

Qué mide
  1. Recuperación: cada sección del documento metodológico sintético (M1-M10) se usa como
     consulta contra (a) la guía sintética sola y (b) la guía + el Anejo 9 de la Circular 4/2017
     (norma pública real, ~350 fragmentos que actúan como distractores). Un fragmento recuperado
     es relevante si pertenece a la guía sintética y contiene al menos el 60% de las palabras
     significativas del requisito etiquetado (gold_req); un fragmento de 800 caracteres suele
     cubrir 2-3 requisitos. Métricas: Hit@1, Hit@3 y MRR@3 sobre M1-M8.
  2. Sin evidencia: similitud del mejor fragmento en M9-M10 (sin requisito aplicable) frente a
     M1-M8, para ver si un umbral podría detectar "no hay información suficiente".
  3. Veredicto del LLM: con el prompt que usa la API para "Normativo vs Funcional" y el contexto
     recuperado de la guía sintética, se clasifica cada respuesta como alineado / no_alineado /
     sin_evidencia con una heurística de palabras clave y, además, con una revisión manual
     (results/revision_manual.json, con justificación por respuesta). Ambas se comparan con
     gold_label; las respuestas completas se guardan en results/llm_<modelo>.json.

Lo que NO permite concluir: el corpus es pequeño (10 secciones) y sintético; los resultados
describen este caso de prueba, no el rendimiento sobre documentación bancaria real.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "IA-modulable"))
sys.path.insert(0, str(ROOT / "examples"))

from langchain_core.documents import Document  # noqa: E402

import synthetic_corpus as corpus  # noqa: E402
from RAG3 import RAG  # noqa: E402
from X_qderant import get_qdrant_client  # noqa: E402

GUIA = ROOT / "examples" / "synthetic" / "normativa_sintetica_pd.pdf"
ANEJO9 = ROOT / "examples" / "public" / "BOE-A-2017-14334_anejo9.pdf"
OUT = ROOT / "eval" / "results"

COLECCIONES = {
    "guia_sintetica": [GUIA],
    "guia_sintetica+anejo9_boe": [GUIA, ANEJO9],
}


def palabras(texto):
    return {w for w in re.findall(r"\w+", texto.lower()) if len(w) > 3}


def requisitos_de(fragmento, umbral=0.6):
    """Requisitos de la guía sintética contenidos en el fragmento (>= umbral de sus palabras)."""
    p = palabras(fragmento)
    cubiertos = []
    for rid, (titulo, texto) in corpus.REQUISITOS.items():
        pr = palabras(f"{titulo} {texto}")
        if len(pr & p) / len(pr) >= umbral:
            cubiertos.append(rid)
    return cubiertos


def indexar(nombre, rutas):
    """Mismo proceso que la API: lectura, limpieza, troceado 800/200 y registro en Qdrant."""
    rag = RAG(str(rutas[0]))
    docs = []
    for ruta in rutas:
        rag.path = str(ruta)
        docs.extend(rag.read_document())
    chunks = rag.split(rag.clean(docs), chunk_ss=800, chunk_so=200)
    t0 = time.time()
    n = rag.qdrant_record(chunks, collection_name=nombre)
    return rag, n, time.time() - t0


def evaluar_recuperacion(rag, coleccion):
    filas = []
    for s in corpus.METODOLOGIA:
        consulta = f"{s['titulo']}\n\n{s['texto']}"
        hits = rag.qdrant.qdrant_search(consulta, k=3, collection_name=coleccion)
        cubiertos = [requisitos_de(h["text"]) if h["filename"] == GUIA.name else [] for h in hits]
        etiquetas = ["+".join(c) if h["filename"] == GUIA.name else "distractor" for c, h in zip(cubiertos, hits)]
        rango = next((i + 1 for i, c in enumerate(cubiertos) if s["gold_req"] in c), None)
        filas.append({"seccion": s["id"], "gold_req": s["gold_req"], "recuperados": etiquetas,
                      "fuentes": [f"{h['filename']} p.{h['page']}" for h in hits],
                      "scores": [round(h["score"], 4) for h in hits], "rango": rango})
    con_gold = [f for f in filas if f["gold_req"]]
    metricas = {
        "n_consultas": len(con_gold),
        "hit@1": sum(f["rango"] == 1 for f in con_gold) / len(con_gold),
        "hit@3": sum(f["rango"] is not None for f in con_gold) / len(con_gold),
        "mrr@3": sum(1 / f["rango"] for f in con_gold if f["rango"]) / len(con_gold),
        "top1_score_con_requisito": [f["scores"][0] for f in con_gold],
        "top1_score_sin_requisito": [f["scores"][0] for f in filas if not f["gold_req"]],
    }
    return filas, metricas


NEG = r"no (se )?(ajusta|alinea|cumple|coincide|est[aá] alinead[oa]|es coherente)|desalinead|incumpl|no hay alineaci"
SIN = (r"no (hay|existe|se encuentra|contiene|se proporciona) (informaci[oó]n|evidencia|relaci[oó]n)|"
       r"no (es posible|se puede) (determinar|evaluar|confirmar|establecer)|no (est[aá]|guarda) relaci|"
       r"no (est[aá]|tiene) relacionad|informaci[oó]n insuficiente")
POS = r"(se ajusta|se alinea|est[aá] alinead[oa]|cumple|coincide|es coherente)"


def clasificar(respuesta):
    """Heurística transparente: gana el patrón que aparece antes en la respuesta."""
    t = respuesta.lower()
    posiciones = {etq: (m.start() if (m := re.search(p, t)) else 10**9)
                  for etq, p in (("sin_evidencia", SIN), ("no_alineado", NEG), ("alineado", POS))}
    etq, pos = min(posiciones.items(), key=lambda kv: kv[1])
    return etq if pos < 10**9 else "indeterminado"


def evaluar_llm(rag, coleccion, modelo):
    import X_AGENT
    from langchain_ollama.llms import OllamaLLM
    from prompt import prompt_definitivos

    agente = X_AGENT.Agente(X_AGENT.ollama_endpoint, modelo)
    agente.set_prompt(prompt_definitivos["evaluar_alineacion_normativa"])  # prompt de "Normativo vs Funcional"
    assert isinstance(agente.llm, OllamaLLM)
    filas = []
    for s in corpus.METODOLOGIA:
        consulta = f"{s['titulo']}\n\n{s['texto']}"
        res = rag.process_query_chunks_v2([Document(page_content=consulta)], collection_name=coleccion)[0]
        t0 = time.time()
        respuesta = agente.get_answer(contexto=res["context"], pregunta=consulta)
        filas.append({"seccion": s["id"], "gold_label": s["gold_label"], "prediccion": clasificar(respuesta),
                      "segundos": round(time.time() - t0, 1), "respuesta": respuesta})
        print(f"   {modelo} {s['id']}: gold={s['gold_label']} pred={filas[-1]['prediccion']} ({filas[-1]['segundos']} s)")
    aciertos = sum(f["prediccion"] == f["gold_label"] for f in filas)
    return filas, {"modelo": modelo, "aciertos": aciertos, "n": len(filas), "accuracy": aciertos / len(filas),
                   "segundos_medios": round(sum(f["segundos"] for f in filas) / len(filas), 1)}


def informe(recuperacion, llm):
    l = ["# Resultados de la evaluación", "",
         "Generado por `eval/run_eval.py`. Corpus sintético (ver `examples/synthetic_corpus.py`): 10 secciones de un",
         "documento metodológico ficticio, 8 con un requisito aplicable en la guía sintética (5 alineadas y 3 con",
         "desviaciones deliberadas) y 2 sin requisito aplicable. Embeddings `nomic-embed-text` (Ollama), Qdrant, top-3.", "",
         "## Recuperación (M1-M8)", "",
         "| Colección de referencia | Fragmentos | Hit@1 | Hit@3 | MRR@3 | Indexación |",
         "|---|---:|---:|---:|---:|---:|"]
    for nombre, r in recuperacion.items():
        m = r["metricas"]
        l.append(f"| {nombre} | {r['n_fragmentos']} | {m['hit@1']:.2f} | {m['hit@3']:.2f} | {m['mrr@3']:.2f} | {r['seg_indexacion']:.0f} s |")
    l += ["", "## Similitud del mejor fragmento: secciones con y sin requisito aplicable", "",
          "| Colección | Con requisito (M1-M8): mín - máx | Sin requisito (M9, M10) |", "|---|---|---|"]
    for nombre, r in recuperacion.items():
        m = r["metricas"]
        con, sin = m["top1_score_con_requisito"], m["top1_score_sin_requisito"]
        l.append(f"| {nombre} | {min(con):.3f} - {max(con):.3f} | {', '.join(f'{x:.3f}' for x in sin)} |")
    if llm:
        manual_path = OUT / "revision_manual.json"
        manual = json.loads(manual_path.read_text(encoding="utf-8")) if manual_path.exists() else {}
        gold = {s["id"]: s["gold_label"] for s in corpus.METODOLOGIA}
        desviados = [s["id"] for s in corpus.METODOLOGIA if s["gold_label"] != "alineado"]
        l += ["", "## Veredicto del LLM (M1-M10, contexto recuperado de la guía sintética)", "",
              "Cada respuesta se clasifica de dos formas: una heurística de palabras clave fijada antes de ver los",
              "resultados y una revisión manual de la respuesta completa (`revision_manual.json`, con justificación).",
              "La revisión manual es la referencia; la tabla muestra también dónde discrepan.", "",
              "| Modelo | Aciertos (manual) | Aciertos (heurística) | Dice \"alineado\" en los 5 casos no alineados o sin requisito | Segundos/respuesta (CPU) |",
              "|---|---:|---:|---:|---:|"]
        for modelo, r in llm.items():
            m = r["metricas"]
            man = manual.get(modelo, {})
            ok_man = sum(man.get(k, [None])[0] == v for k, v in gold.items()) if man else None
            falsos = sum(man.get(k, [None])[0] == "alineado" for k in desviados) if man else None
            l.append(f"| {modelo} | {ok_man if man else '-'}/{m['n']} | {m['aciertos']}/{m['n']} | "
                     f"{falsos if man else '-'}/{len(desviados)} | {m['segundos_medios']} |")
        cab = " | ".join(f"{mod} (heur.) | {mod} (manual)" for mod in llm)
        l += ["", f"| Sección | Esperado | {cab} |", "|---|---|" + "---|---|" * len(llm)]
        for i, s in enumerate(corpus.METODOLOGIA):
            celdas = " | ".join(f"{r['filas'][i]['prediccion']} | {manual.get(mod, {}).get(s['id'], ['-'])[0]}"
                                for mod, r in llm.items())
            l.append(f"| {s['id']} {s['titulo']} | {s['gold_label']} | {celdas} |")
        l += ["", "Las respuestas completas están en `llm_<modelo>.json`. El modelo de 1B a menudo repite la plantilla",
              "del prompt antes de responder."]
    return "\n".join(l) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="*", default=["llama3.2:1b"], help="modelos de Ollama para el veredicto")
    ap.add_argument("--sin-llm", action="store_true", help="solo recuperación; reutiliza results/llm_*.json en el informe")
    args = ap.parse_args()
    if not ANEJO9.exists():
        raise SystemExit("Falta el Anejo 9: ejecuta antes python examples/public/download_anejo9.py")

    OUT.mkdir(parents=True, exist_ok=True)
    cliente = get_qdrant_client()
    recuperacion, rags = {}, {}
    for nombre, rutas in COLECCIONES.items():
        coleccion = "eval_" + re.sub(r"\W", "_", nombre)
        if cliente.collection_exists(coleccion):
            cliente.delete_collection(coleccion)  # indexación limpia y tiempo medido en cada ejecución
        rag, n, seg = indexar(coleccion, rutas)
        filas, metricas = evaluar_recuperacion(rag, coleccion)
        recuperacion[nombre] = {"coleccion": coleccion, "n_fragmentos": n, "seg_indexacion": round(seg, 1),
                                "metricas": metricas, "filas": filas}
        rags[nombre] = (rag, coleccion)
        print(f"📊 {nombre}: hit@1={metricas['hit@1']:.2f} hit@3={metricas['hit@3']:.2f} mrr={metricas['mrr@3']:.2f}")
    (OUT / "recuperacion.json").write_text(json.dumps(recuperacion, ensure_ascii=False, indent=2), encoding="utf-8")

    llm = {}
    if args.sin_llm:  # reutiliza los veredictos ya calculados para el informe
        for f in sorted(OUT.glob("llm_*.json")):
            datos = json.loads(f.read_text(encoding="utf-8"))
            llm[datos["metricas"]["modelo"]] = datos
    else:
        rag, coleccion = rags["guia_sintetica"]
        for modelo in args.modelos:
            filas, metricas = evaluar_llm(rag, coleccion, modelo)
            llm[modelo] = {"metricas": metricas, "filas": filas}
            nombre = re.sub(r"\W", "_", modelo)
            (OUT / f"llm_{nombre}.json").write_text(json.dumps(llm[modelo], ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"🤖 {modelo}: {metricas['aciertos']}/{metricas['n']} aciertos")
    (OUT / "README.md").write_text(informe(recuperacion, llm), encoding="utf-8")
    print("✅ Informe en eval/results/README.md")

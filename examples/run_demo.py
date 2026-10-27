"""Demo de extremo a extremo contra la API (POST /validar) con los documentos sintéticos.

Requiere Ollama (nomic-embed-text + llama3.2:1b), Qdrant y la API en marcha (ver README).

    python examples/run_demo.py                 # 4 tipos de validación, con veredicto del LLM
    python examples/run_demo.py --sin-agente    # solo recuperación (rápido, sin LLM)
    python examples/run_demo.py --solo "Normativo vs Funcional"

Guarda las respuestas en examples/outputs/<tipo>.json y un resumen legible en <tipo>.md.
"""
import argparse
import json
import os
import time
import unicodedata
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "synthetic"
OUT = ROOT / "outputs"

NORMATIVA = DOCS / "normativa_sintetica_pd.pdf"
METODOLOGIA = DOCS / "metodologia_banco_ficticio.docx"
TECNICO = DOCS / "tecnico_banco_ficticio.docx"
SAS = DOCS / "codigo_pd_ficticio.sas"

# (tipo de validación, documentos de referencia, documento a validar, colección)
FLUJOS = [
    ("Normativo vs Funcional", [NORMATIVA], METODOLOGIA, "demo_normativa"),
    ("Funcional vs Técnico", [METODOLOGIA], TECNICO, "demo_metodologia"),
    ("Código vs Técnico", [TECNICO], SAS, "demo_tecnico"),
    ("Código vs Estadístico", [NORMATIVA], SAS, "demo_normativa"),
]


def validar(api_url, tipo, refs, consulta, coleccion, usar_agente):
    files = [("file_ref", (p.name, p.read_bytes())) for p in refs]
    files.append(("file_query", (consulta.name, consulta.read_bytes())))
    data = {"collection_name": coleccion, "doc_sample_ratio": 1.0,
            "usar_agente": str(usar_agente).lower(), "tipo_validacion": tipo}
    r = requests.post(f"{api_url}/validar", files=files, data=data, timeout=3600)
    if r.status_code != 200:
        raise SystemExit(f"Error {r.status_code} en '{tipo}': {r.text}")
    return r.json()["resultados"]


def a_markdown(tipo, refs, consulta, resultados, segundos):
    lineas = [f"# {tipo}", "",
              f"- Referencia: {', '.join(p.name for p in refs)}",
              f"- Documento validado: {consulta.name}",
              f"- Fragmentos analizados: {len(resultados)} · tiempo total: {segundos:.0f} s", ""]
    for i, r in enumerate(resultados, 1):
        lineas += [f"## Fragmento {i}", "", "**Fragmento validado:**", "", "> " + r["chunk"].replace("\n", "\n> "), ""]
        lineas.append("**Evidencias recuperadas (fuente · página · similitud coseno):**")
        lineas.append("")
        for txt, src, score in zip(r["relevant_chunks"], r.get("sources", []), r.get("scores", [])):
            pagina = f" · p.{src['page']}" if src.get("page") else ""
            lineas.append(f"- `{src['filename']}{pagina} · {score:.3f}` — {txt[:220].replace(chr(10), ' ')}…")
        if "respuesta" in r:
            lineas += ["", "**Veredicto del LLM:**", "", r["respuesta"].strip()]
        lineas.append("")
    return "\n".join(lineas)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-url", default=os.getenv("API_URL", "http://localhost:8000"))
    ap.add_argument("--sin-agente", action="store_true", help="no llamar al LLM (solo recuperación)")
    ap.add_argument("--solo", help="ejecutar solo este tipo de validación")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    for tipo, refs, consulta, coleccion in FLUJOS:
        if args.solo and args.solo != tipo:
            continue
        t0 = time.time()
        resultados = validar(args.api_url, tipo, refs, consulta, coleccion, not args.sin_agente)
        segundos = time.time() - t0
        slug = unicodedata.normalize("NFKD", tipo.lower()).encode("ascii", "ignore").decode().replace(" ", "_")
        sufijo = "_sin_agente" if args.sin_agente else ""
        (OUT / f"{slug}{sufijo}.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / f"{slug}{sufijo}.md").write_text(a_markdown(tipo, refs, consulta, resultados, segundos), encoding="utf-8")
        print(f"✅ {tipo}: {len(resultados)} fragmentos en {segundos:.0f} s -> examples/outputs/{slug}{sufijo}.md")

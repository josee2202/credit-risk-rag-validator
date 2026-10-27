"""Descarga el Anejo 9 de la Circular 4/2017 del Banco de España desde la fuente oficial (BOE).

    python examples/public/download_anejo9.py

Descarga la disposición completa BOE-A-2017-14334 (~39 MB, 588 páginas) y guarda solo las
55 páginas del Anejo 9 ("Análisis y cobertura del riesgo de crédito", págs. 119987-120041 del
BOE núm. 296, de 6 de diciembre de 2017) en examples/public/BOE-A-2017-14334_anejo9.pdf.
El PDF no se versiona: fuente oficial https://www.boe.es/eli/es/cir/2017/11/27/4
"""
import tempfile
from pathlib import Path

import requests
from pypdf import PdfReader, PdfWriter

URL = "https://www.boe.es/boe/dias/2017/12/06/pdfs/BOE-A-2017-14334.pdf"
PRIMERA, ULTIMA = 533, 587  # índices (base 0) de las páginas del Anejo 9 en el PDF oficial
DESTINO = Path(__file__).resolve().parent / "BOE-A-2017-14334_anejo9.pdf"

if __name__ == "__main__":
    if DESTINO.exists():
        print("Ya existe:", DESTINO)
        raise SystemExit(0)
    with tempfile.TemporaryDirectory() as tmp:
        completo = Path(tmp) / "BOE-A-2017-14334.pdf"
        print("Descargando", URL)
        r = requests.get(URL, timeout=300)
        r.raise_for_status()
        completo.write_bytes(r.content)
        reader = PdfReader(completo)
        if "ANEJO 9" not in reader.pages[PRIMERA].extract_text():
            raise SystemExit("El PDF descargado no tiene el formato esperado (¿ha cambiado el BOE?)")
        writer = PdfWriter()
        for i in range(PRIMERA, ULTIMA + 1):
            writer.add_page(reader.pages[i])
        writer.write(DESTINO)
    print(f"✅ Anejo 9 guardado en {DESTINO} ({ULTIMA - PRIMERA + 1} páginas)")

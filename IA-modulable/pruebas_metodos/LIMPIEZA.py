

import spacy
import string

# Cargar spaCy (puedes mover esto al constructor si lo prefieres)
nlp = spacy.load("es_core_news_sm")

class Limpieza: 
    def __init__(self):
        pass

    def stop_words(texto):
        # * Eliminar stopwords y puntuación usando spaCy
        doc = nlp(texto)
        texto_filtrado = [token.text for token in doc if not token.is_stop and not token.is_punct]
        texto_limpio = " ".join(texto_filtrado)

        print("Stopwords eliminadas del texto completo del documento.")
        return texto_limpio

    def normalize_text(texto):
        """
        Normaliza el texto convirtiéndolo a minúsculas y eliminando caracteres especiales irrelevantes.
        Conserva todos los números.
        """
        # Convertir a minúsculas
        texto = texto.lower()

        # Eliminar caracteres especiales irrelevantes (excepto números)
        texto = texto.translate(str.maketrans("", "", string.punctuation))

        # ? Valorar añadir una parte del proceso para los números --> CUIDADO

        return texto
    
    def lematizar(texto):
        """
        Lematiza un texto dado utilizando spaCy.

        Args:
            texto (str): Texto a lematizar.

        Returns:
            str: Texto lematizado.
        """
        doc = nlp(texto)
        lemas = [token.lemma_ for token in doc]
        return " ".join(lemas)
    
    def reconocer_entidades(texto):
        """
        Identifica y clasifica entidades nombradas en un texto dado utilizando spaCy.

        Args:
            texto (str): Texto a analizar.

        Returns:
            list: Lista de tuplas (entidad, tipo).
        """
        doc = nlp(texto)
        entidades = [(ent.text, ent.label_) for ent in doc.ents]
        return entidades
    



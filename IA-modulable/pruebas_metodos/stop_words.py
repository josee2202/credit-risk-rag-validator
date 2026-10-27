import spacy

nlp = spacy.load('es_core_news_sm')     # * Este modelo es para el español, hay que descargarlo desde terminal 
texto = "Este es otro ejemplo de texto para procesar."
doc = nlp(texto)
texto_filtrado = [token.text for token in doc if not token.is_stop]
print(texto_filtrado)



# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# texto = "Este es un ejemplo de texto para eliminar stopwords."
# palabras = word_tokenize(texto, language='spanish')
# stop_words = set(stopwords.words('spanish'))
# texto_filtrado = [palabra for palabra in palabras if palabra.lower() not in stop_words]

# print(texto_filtrado)
def eliminar_stopwords(texto):
    """
    Elimina las stopwords de un texto dado utilizando spaCy.

    Args:
        texto (str): El texto del que se eliminarán las stopwords.

    Returns:
        str: Texto sin stopwords.
    """
    # Procesar el texto con spaCy
    doc = nlp(texto)
    
    # Filtrar tokens que no sean stopwords ni puntuación
    texto_filtrado = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
    # Unir los tokens filtrados en un solo string
    return " ".join(texto_filtrado)

# Ejemplo de uso
texto_original = "Este es un ejemplo de texto para eliminar stopwords."
texto_limpio = eliminar_stopwords(texto_original)
print("Texto original:", texto_original)
print("Texto limpio:", texto_limpio)
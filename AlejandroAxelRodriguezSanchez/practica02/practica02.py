# -*- coding: utf-8 -*-
"""Practica02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i8HlQRHosBWRCezBaprNQXBK_5V-AFvD

# Práctica 2: Morfología y análisis morfógico

Elaborado por: Alejandro Axel Rodríguez Sánchez  
Correo: [ahexo@ciencias.unam.mx](mailto:ahexo@ciencias.unam.mx)  
Github: [@Ahexo](https://github.com/Ahexo/)  
Número de Cuenta: 315247697  
Institución: Facultad de Ciencias UNAM  
Asignatura: Lingüística computacional  
Grupo: 7014  
Semestre: 2024-1

En esta práctica vamos a realizar los tres procedimientos fundamentales de análisis morfológico en un conjunto específico de oraciones. Estos procedimientos son:

- Stemming (con ayuda de la biblioteca nltk)
- Lemmatization (empleando spacy)
- Obtención de información morfologica (también con spacy)

Como vamos a utilizar el corpus del [*SIGMORPHON 2022 Shared Task on Morpheme Segmentation*](https://github.com/sigmorphon/2022SegmentationST/tree/main). La única lengua con soporte a lo largo de los tres (este corpus y las facilidades de spacy y nltk) es el inglés, de donde vamos a extraer nuestras oraciones.
"""

# Importamos las bibliotecas requeridas.

# Utilidades para procesar cadenas, contenerlas y mostrar resultados en pantalla
import random
import requests
import pandas as pd


# Para hacer stemming sobre oraciones en inglés
from nltk.stem.snowball import EnglishStemmer
stemmer = EnglishStemmer()

from nltk.tokenize import wordpunct_tokenize

# Para lematizar y obtener información morfológica
import spacy
nlp = spacy.load('en_core_web_sm')

"""Agregamos un par de funciones auxiliares extraídas de la especificación de la práctica."""

def get_files(lang: str, track: str = "word") -> list[str]:
    """
    Genera una lista de nombres de archivo basados en el idioma y el track

    Parameters:
    ----------
    lang : str
        Idioma para el cual se generarán los nombres de archivo.
    track : str, optional
        Track del shared task de donde vienen los datos (por defecto es "word").

    Returns:
    -------
    list of str
        Una lista de nombres de archivo generados para el idioma y la pista especificados.
    """
    return [
        f"{lang}.{track}.test.gold",
        f"{lang}.{track}.dev",
    ]

def get_raw_corpus(files: list) -> list:
    """
    Descarga y concatena los datos de los archivos tsv desde una URL base.

    Parameters:
    ----------
    files : list
        Lista de nombres de archivos (sin extensión) que se descargarán
        y concatenarán.

    Returns:
    -------
    list
        Una lista que contiene los contenidos descargados y concatenados
        de los archivos tsv.
    """
    result = []
    for file in files:
        print(f"Downloading {file}.tsv")
        r = requests.get(f"https://raw.githubusercontent.com/sigmorphon/2022SegmentationST/main/data/{file}.tsv")
        response_list = r.text.split("\n")
        result.extend(response_list[:-1])
    return result

def raw_corpus_to_dataframe(corpus_list: list, lang: str) -> pd.DataFrame:
    """
    Convierte una lista de datos de corpus en un DataFrame

    Parameters:
    ----------
    corpus_list : list
        Lista de líneas del corpus a convertir en DataFrame.
    lang : str
        Idioma al que pertenecen los datos del corpus.

    Returns:
    -------
    pd.DataFrame
        Un DataFrame de pandas que contiene los datos del corpus procesados.
    """
    data_list = []
    for line in corpus_list:
        try:
            word, tagged_data, category = line.split("\t")
        except ValueError:
            # Caso donde no existe la categoria
            word, tagged_data = line.split("\t")
            category = "NOT_FOUND"
        morphemes = tagged_data.split()
        stem = morphemes[0]
        data_list.append({"words": word, "stems": stem, "morph": morphemes, "category": category, "lang": lang})
    df = pd.DataFrame(data_list)
    df["word_len"] = df["words"].apply(lambda x: len(x))
    df["stem_len"] = df["stems"].apply(lambda x: len(x))
    df["morph_len"] = df["morph"].apply(lambda x: len(x))
    return df

"""Ahora definimos nuevas funciones para realizar la tarea asignada:"""

def pick_raw_sentences(quantity: int, lang_id: str):
    """
    Selecciona un número arbitrario de oraciones al azar de un corpus
    en un idioma en particular.

    Parameters:
    ----------
    quantity : int
        Número de oraciones.
    lang_id : str
        Identificador ISO de la lengua, tiene que estar en el repo de
        sigmorphon/2022SegmentationST.

    Returns:
    -------
    list of str
      Lista con las oraciones obtenidas.
    """
    # Importamos el archivo crudo del corpus.
    files = get_files(lang_id, 'sentence')
    print('files', files)

    # Seleccionamos un número arbitrario de lineas del corpus.
    raw = get_raw_corpus([files[1]])
    lines = random.sample(raw, quantity)
    sentences = []

    # Procesamos las líneas obrenidas.
    for line in lines:
        sentence, tagged = line.split("\t")
        sentences.append(sentence)

    return sentences

def analyze_word_eng(word: str):
    """
    Recibe una palabra en inglés, le sacamos la raíz con nltk
    y la lematizamos.

    Parameters:
    ----------
    word : str
        Palabra en inglés a analizar.

    Returns:
    -------
    dict
      Diccionario con la palabra, la raíz, su lematización y la información mofológica.
    """

    result = {}
    result['palabra'] = word

    result['raiz'] = stemmer.stem(word)

    tokens = nlp(word)
    result['lema'] = tokens[0].lemma_

    result['info_morfologica'] = tokens[0].morph.to_dict()

    return result

def analyze_sentence_eng(sentence: str):
    """
    Recibe una oración en inglés, la *tokenizamos* con nltk y le hacemos
    análisis a cada una de sus palabras.

    Parameters:
    ----------
    sentence : str
        Oración a analizar.

    Returns:
    -------
    list of str
      Lista con las oraciones obtenidas.
    """
    words = wordpunct_tokenize(sentence)

    result = []
    for word in words:
        result.append(analyze_word_eng(word))

    return result

"""Finalmente, desplegamos resultados para 10 oraciones en pantalla:"""

sentences = pick_raw_sentences(10, 'eng')

count = 0
for sentence in sentences:
    count += 1

    analisis = analyze_sentence_eng(sentence)
    reporte = pd.DataFrame(analisis)

    print(f'Oración {count}:', sentence)
    print(reporte, '\n')
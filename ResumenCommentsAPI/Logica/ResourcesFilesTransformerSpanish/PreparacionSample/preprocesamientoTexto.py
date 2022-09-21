import numpy as np
import pandas as pd 
import re
from bs4 import BeautifulSoup
import string

def eliminarValoresNulos(dataset):
    """
        Funcion para eliminar valores nulos del dataset
        Args:
            dataset (dataframe): dataset con comentario
        return: 
            dataset: sin valores nulos
    """
    nan_rows = dataset[dataset.isnull().any(1)]
    dataset.columns[dataset.isnull().any()]
    dataset = dataset.dropna(how='any')
    return dataset

def limpiarTexto(texto):
    """
        Funcion que lleva a cabo toda la limpieza de nuestro comentario
        Args:
            texto (string): comentario sin realizar ninguna limpieza
        return:
            newString: comentario  ya con limpieza realizada
    """
    newString = texto.lower() #texto en minisculas 
    newString = BeautifulSoup(newString, "html.parser").text # eliminacion de texto html
    newString = re.sub(r'\([^)]*\)', '', newString) #eliminacion de caracteres especiales
    newString = re.sub('"','', newString) #eliminacion de comillas dentro del texto
    newString = re.sub('[m]{2,}', 'mm', newString) 
    '''elimine el texto entre corchetes, elimine la puntuación y elimine las palabras que contienen números.'''
    newString = re.sub('\[.*?¿\]\%', ' ', newString)
    newString = re.sub('[%s]' % re.escape(string.punctuation), ' ', newString)
    newString = re.sub('\w*\d\w*', '', newString)
    '''Deshágase de algunos signos de puntuación adicionales y texto sin sentido que se perdió la primera vez.'''
    newString = re.sub('[‘’“”…«»]', '', newString)
    newString = re.sub('\n', ' ', newString)
    return newString

def limpiarNewSample(dataset):
    """
        Funcion que lleva a cabo toda la limpieza de todo el dataset
        Args:
            dataset (dataframe): todos los comentarios
        return:
            dataset: comentarios ya limpios
    """
    ## Limpiamos el texto de la columna text 
    textoLimpio = []
    for t in dataset['Text']:
        newtextoLimpio = limpiarTexto(t)
        textoLimpio.append(newtextoLimpio) 
    dataset['cleaned_text']=textoLimpio
    return dataset

def TextoToDataframe(texto):
    """
        Funcion para convertir de texto a dataframe
        Args:
            texto (string): comentarios
        return:
            dataset: dataset con comentario
    """
    listadoTexto = [texto]
    datasetPredict = pd.DataFrame()
    datasetPredict['Text'] = listadoTexto
    return datasetPredict
import numpy as np
import pandas as pd 
import re
from bs4 import BeautifulSoup
import string
import nltk
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('es_core_news_sm')

nltk.download('stopwords')
stop_words = set(stopwords.words('spanish')) 

def eliminarValoresNulos(dataset):
    nan_rows = dataset[dataset.isnull().any(1)]
    dataset.columns[dataset.isnull().any()]
    dataset = dataset.dropna(how='any')
    return dataset

def limpiarTexto(texto):
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

def limpiarDataset(dataset):
    ## Limpiamos el texto de la columna text 
    textoLimpio = []
    for t in dataset['comentario_completo']:
        newtextoLimpio = limpiarTexto(t)
        textoLimpio.append(newtextoLimpio) 
        
    ## Limpiamos el texto de la columna Summary 
    summarylimpio = []
    for t in dataset['resumen_comentario']:
        newSummaryLimpio = limpiarTexto(t)
        summarylimpio.append(newSummaryLimpio)
        
    dataset=dataset.assign(cleaned_text=textoLimpio)
    dataset=dataset.assign(cleaned_summary=summarylimpio)
    return dataset

def stopWords(textoLimpio, numero):
    if(numero==0):
        tokens = [w for w in textoLimpio.split() if not w in stop_words]
    else:
        tokens=textoLimpio.split()
    long_words=[]    
    for i in tokens:
        if len(i)>1:  #eliminacion de palabras cortas
            long_words.append(i)   
    return (" ".join(long_words)).strip()
    
def stopWords_dataset(datasetLimpio):
    ## Limpiamos el texto de la columna text 
    textoToken = []
    for t in datasetLimpio['cleaned_text']:
        newtextoToken = stopWords(t,0)
        textoToken.append(newtextoToken) 
        
    ## Limpiamos el texto de la columna Summary 
    summaryToken = []
    for t in datasetLimpio['cleaned_summary']:
        newSummaryToken = stopWords(t,1)
        summaryToken.append(newSummaryToken)
        
    datasetLimpio=datasetLimpio.assign(token_text=textoToken)
    datasetLimpio=datasetLimpio.assign(token_summary=summaryToken)
    return datasetLimpio

def lematizacion(texto):
    doc = nlp(texto)
    lemmas = [tok.lemma_.lower() for tok in doc]
    return (" ".join(lemmas)).strip()

def lematizacion_dataset(dataToken):
    ## Limpiamos el texto de la columna text 
    textoLema = []
    for t in dataToken['token_text']:
        newtextoToken = lematizacion(t)
        textoLema.append(newtextoToken) 
        
    ## Limpiamos el texto de la columna Summary 
    summaryLema = []
    for t in dataToken['token_summary']:
        newSummaryToken = lematizacion(t)
        summaryLema.append(newSummaryToken)

    dataToken=dataToken.assign(lema_text=textoLema)
    dataToken=dataToken.assign(lema_summary=summaryLema)

    return dataToken

def procesamientoLimpieza(data):
    #comentar si se quiere eliminar todos los comenatios con algun valor nulo, tanto en columnas o filas
    data = eliminarValoresNulos(data)
    data = limpiarDataset(data)
    data = stopWords_dataset(data)
    data = lematizacion_dataset(data)
    data.reset_index(drop=True, inplace=True)
    return data

from cmath import log
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from ...Logica.TopicModelPython.topic_model_LSA import topicLSA
def usuariosByGenero(data):
    df = data
    dict = {}
    try:
        dict['Hombres'] = (df["genero"].value_counts())['Hombres']
    except:
         dict['Hombres'] = 0

    try:
         dict['Mujeres'] = (df["genero"].value_counts())['Mujeres']
    except:
         dict['Mujeres'] = 0

    try:
         dict['lgbtiq+'] = (df["genero"].value_counts())['lgbtiq+']
    except:
         dict['lgbtiq+'] = 0
    
    distribucion = [(clave, valor) for clave, valor in dict.items()]
    df = pd.DataFrame(distribucion, columns = [ 'genero', 'count'])
    return df


def sentimientoDeComentario(data):
    df = data
    dict = {}
    try:
        dict['MuyBueno'] = (df["tipo_comentario"].value_counts())['very positive']
    except:
        dict['MuyBueno'] = 0
    try:
        dict['Bueno'] = (df["tipo_comentario"].value_counts())['positive']
    except:
        dict['Bueno'] = 0
    try:
        dict['Neutro'] = (df["tipo_comentario"].value_counts())['mixed']
    except:
        dict['Neutro'] = 0
    try:
        dict['Malo'] = (df["tipo_comentario"].value_counts())['negative']
    except:
        dict['Malo'] = 0
    try:
        dict['MuyMalo'] = (df["tipo_comentario"].value_counts())['very negative']
    except:
        dict['MuyMalo'] = 0

    distribucion = [(clave, valor) for clave, valor in dict.items()]
    df = pd.DataFrame(distribucion, columns = [ 'sentimiento', 'count'])
    return df

def comentariosAtravesTiempo(data):
    df = data
    df['fecha_comentario'] = pd.to_datetime(df['fecha_comentario'], format="%Y-%m-%dT%H:%M:%S.%f")
    df['Year'] = df['fecha_comentario'].dt.year 
    df['Month'] = df['fecha_comentario'].dt.month 
    df['Day'] = df['fecha_comentario'].dt.day
    
    dict = {}
    listayear = df['Year'].unique()
    listames = df['Month'].unique()
    listadia = df['Day'].unique()
    tipoCommentario = ['very positive', 'positive', 'mixed', 'negative', 'very negative']
    valores = []
    for year in listayear:
        for mes in listames:
            for dia in listadia:
                for tipo in tipoCommentario:
                    valor = df.loc[(df["tipo_comentario"]==tipo) & (df["Day"]==dia )& (df["Month"]==mes ) & (df["Year"]==year )].count()[0]
                    fecha = str(year)+"-"+str(mes)+"-"+str(dia) 
                    valores.append((fecha, tipo, valor))
    df = pd.DataFrame(valores, columns = [ 'fecha', 'tipo', 'valor'])
    return df



def print_top_words(model, feature_names, n_top_words):
    listaTopics = []
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += ", ".join([feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]])
        message += " ==> "+str(len(topic.argsort()))
        print(message)
    
    

def generandoTopicDatasetComentarios(data, tipoDocument):
    valores = topicLSA(data, tipoDocument)
    df = pd.DataFrame(valores, columns = [ 'labels', 'categorias', 'valores'])
    return df


def usuariosPorEdades(data):
    df = data
    
    valorIndex = (df['edad'].value_counts())
    valorEdad = valorIndex.tolist()
    dictV = {}
    for x in range(0,len(valorEdad)):
        dictV[int(valorIndex.index[x])] = valorEdad[x]
    dict = {}
    dict['0-10'] = 0
    dict['10-20'] = 0
    dict['20-30'] = 0
    dict['30-40'] = 0
    dict['40-50'] = 0
    dict['50-60'] = 0
    dict['60-70'] = 0
    dict['70-100'] = 0

    for key, value in dictV.items():
        
        if(key >= 0 and key < 10): 
            dict['0-10'] = dict['0-10'] + value
        elif(key >= 10 and key < 20):
            dict['10-20'] = dict['10-20'] + value
        elif(key >= 20 and key < 30):
            dict['20-30'] = dict['20-30'] + value
        elif(key >= 30 and key < 40):
            dict['30-40'] = dict['30-40'] + value
        elif(key >= 40 and key < 50):
            dict['40-50'] = dict['40-50'] + value
        elif(key >= 50 and key < 60):
            dict['50-60'] = dict['50-60'] + value
        elif(key >= 60 and key < 70):
            dict['60-70'] = dict['60-70'] + value
        elif(key >= 70 and key < 100):
            dict['70-100'] = dict['70-100'] + value
    distribucion = [(clave, valor) for clave, valor in dict.items()]
    df = pd.DataFrame(distribucion, columns = [ 'rango', 'count'])
    return df



def vectorizacionPalabras(corpus, ngrama,n):
    vec = CountVectorizer(ngram_range=(ngrama, ngrama)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def obtener_top_n_words(data, type, ngrama,n=10):
    common_words = vectorizacionPalabras(data[type], ngrama, n)
    df = pd.DataFrame(common_words, columns = [ type, 'count'])
    df.groupby(type).sum()['count'].sort_values(ascending=False)
    dict = {}
    for fila in df.index:
        dict[df[type][fila]] =  df['count'][fila]
    return df
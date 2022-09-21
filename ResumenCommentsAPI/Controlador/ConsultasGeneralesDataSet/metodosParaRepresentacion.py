from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from ...Logica.TopicModelPython.topic_model_LSA import topicLSA


def usuariosByGenero(data):
    """
        Funcion para obtener cuantos hombres, mujeres y cominidad LGBT hay dentro de nuestra aplicacion
        Args:
            data(dataframe): data en donde se encuentran todos los usuarios de nuestra aplicacion 
        return: 
            dataframe: genero con cantidad de cada uno 
    """
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
    """
        Funcion para obtener cuantos valores tiene cada tipo de comentario dentro de nuestros comentarios
        Args:
            data(dataframe): data en donde se encuentran todos los comentarios de nuestra aplicacion 
        return: 
            dataframe: sentimiento con cantidad de cada uno 
    """
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
    """
        Funcion para analizar los comentarios a traves del tiempo, cuantos comentarios por dia
        Args:
            data(dataframe): data en donde se encuentran todos los comentarios de nuestra aplicacion 
        return: 
            dataframe: de lo comentarios a traves de fecha, sentimiento, cantidad de comentarios
    """
    df = data
    ##Convertimos las fecha a formato de fecha
    df['fecha_comentario'] = pd.to_datetime(df['fecha_comentario'], format="%Y-%m-%dT%H:%M:%S.%f")
    ##Creando una columna para cada año, mes y dia
    df['Year'] = df['fecha_comentario'].dt.year 
    df['Month'] = df['fecha_comentario'].dt.month 
    df['Day'] = df['fecha_comentario'].dt.day
    ##Valores unicos para cada fecha
    listayear = df['Year'].unique()
    listames = df['Month'].unique()
    listadia = df['Day'].unique()
    ##Tipos de sentimientos
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

    
def generandoTopicDatasetComentarios(data, tipoDocument):
    """
        Funcion en donde se puede obtener los temas que mas aparaciones se tienen dentro de los comentarios
        ********TODAVIA por mejorar e implementar de mejor manera*******
        Args:
            data(dataframe): data en donde se encuentran todos los comentarios de nuestra aplicacion 
            tipoDocument(columna): tipo de columna con la que se trabaja: resumen o comentario completo
        return: 
            dataframe: de lo comentarios a traves de fecha, sentimiento, cantidad de comentarios
    """
    ##Mejorar y analizar este modelo de machine learning 
    valores = topicLSA(data, tipoDocument)
    ##Creando dataframe con resultados
    df = pd.DataFrame(valores, columns = [ 'labels', 'categorias', 'valores'])
    return df


def usuariosPorEdades(data):
    """
        Funcion para obtener cuantas personas existen por cada rango de edad
        Args:
            data(dataframe): data en donde se encuentran todos los usuarios de nuestra aplicacion 
        return: 
            dataframe: Rango de edad con la cantidad de personas en cada uno
    """
    df = data
    ##Obteniendo la cantidad de edades con sus aparaciones dentro de los usuarios
    valorIndex = (df['edad'].value_counts())
    ##Transformando a listas
    valorEdad = valorIndex.tolist()
    dictV = {}
    ##Creando diccionario con valores unicos
    for x in range(0,len(valorEdad)):
        dictV[int(valorIndex.index[x])] = valorEdad[x]
    ##Rango de edades
    dict = {}
    dict['0-10'] = 0
    dict['10-20'] = 0
    dict['20-30'] = 0
    dict['30-40'] = 0
    dict['40-50'] = 0
    dict['50-60'] = 0
    dict['60-70'] = 0
    dict['70-100'] = 0
    ##Llenando nuestro diccionario con la cantidad de aparaciones
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
    ##Creando dataframe
    distribucion = [(clave, valor) for clave, valor in dict.items()]
    df = pd.DataFrame(distribucion, columns = [ 'rango', 'count'])
    return df



def vectorizacionPalabras(corpus, ngrama,n):
    """
        Funcion para obtecion de n palabras con mas frecuencia dentro de nuestro dataset
        Args:
            corpus(dataframe): data en donde se encuentran todos los comentarios de nuestra aplicacion 
            ngrama(int): cantidad de palabras unidad unigrama, bigrama, ....
            n(int): cantidad de palabras a obtener
        return: 
            words_freq(list): lista ordena con las palabras con mas aparicion
    """
    vec = CountVectorizer(ngram_range=(ngrama, ngrama)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def obtener_top_n_words(data, type, ngrama,n=10):
    """
        Funcion para obtecion de 10 palabras con mas frecuencia dentro de nuestro dataset
        Args:
            data(dataframe): data en donde se encuentran todos los comentarios de nuestra aplicacion 
            type(string): columnas segun el tipo de dataframe resumen o comentario completos
            ngrama(int): cantidad de palabras unidad unigrama, bigrama, ....
            n(int): cantidad de palabras a obtener
        return: 
            dataframe: dataset con las palabras con mas aparicion y su valor de frecuencia
    """
    common_words = vectorizacionPalabras(data[type], ngrama, n)
    ##Creando dataframe con las palabras y cantidad
    df = pd.DataFrame(common_words, columns = [ type, 'count'])
    df.groupby(type).sum()['count'].sort_values(ascending=False)
    dict = {}
    for fila in df.index:
        dict[df[type][fila]] =  df['count'][fila]
    return df
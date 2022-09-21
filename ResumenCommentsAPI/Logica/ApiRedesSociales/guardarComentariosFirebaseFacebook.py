import requests
import json
import time 
import pandas as pd
from ResumenCommentsAPI.Logica.ResourcesFilesTransformerSpanish.Summarization import SummarizationPredict
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
import dateutil.parser as dateparser
from ...ClavesPrivadas.FacebookAPI import TOKEN_RAPID_API

def obtenerTipoComentario(comentario):
    """
        Funciona para obtencion del tipo de comentario extraido de facebook
        Args:
            comentario (string): comentario obtenido de facebook
        return: 
            string: tipo de comentario realizado
    """
    url = "https://multilingual-sentiment-analysis2.p.rapidapi.com/sentiment/multilingual/1.0/classify"
    headers = {
            'content-type': 'application/json',
            'X-RapidAPI-Key': str(TOKEN_RAPID_API),
            'X-RapidAPI-Host': 'multilingual-sentiment-analysis2.p.rapidapi.com',
          }
    data= {'text': comentario}
    output = requests.post(url, data=json.dumps(data), headers=headers).json()
    try:
       return output['label']
    except:
        return None
    
def guardarComentarioFirebase(comentario, correo, fecha, idPost, categoriaComentario,nombreProducto, imagen):
    """
        Funciona para guardar el comentario extraido de facebook
        Args:
            comentario (string): comentario obtenido de facebook
            correo (string): correo de la persona del comentario facebook
            fecha (string): fecha del comentario obtenido de facebook
            idPost (string): id del comentario obtenido de facebook
            categoriaComentario (string): categoria del producto publicado en facebook
            nombreProducto (string): nombre del producto publicado en facebook
            imagen (string): url de imagen del producto publicado en facebook
        return: 
            almacenamiento en logs. 
    """

    ##Verificamos si existe este comentario dentro de firebase para no duplicar información
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'idPost', u'==', idPost).stream()
    verificacion = next(docs, None)
    
    if(verificacion == None):
        ##Obtenido el tipo de comentario mediante API
        tipoComentario = obtenerTipoComentario(comentario)
        ##Obteniendo el resumen del comentario
        resumen_Comentario = SummarizationPredict().predictSummarization(comentario)
        ##Almacenamiento en la base de datos en la nube
        data = {"correo_comentario":correo,
                "comentario_completo": comentario, 
                "tipo_comentario":tipoComentario, 
                "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": dateparser.parse(fecha),
                "idPost": idPost,
                "RedSocial":"Facebook", 
                'categoriaComentario': categoriaComentario,  
                'nombreProducto': nombreProducto, 
                'imagen': imagen
                }
        ##Almacenado el comentario
        CLOUD_DATABASE.collection("Comentario").document(idPost).set(data)
        ##Esto debido a que la api de clasificacion realiza 3 consultas por minuto, en el plan sin costo 
        time.sleep(15)
        ##Modificar esto para guardar resultados en logs
        print("Archivo Guardado :) ")
    else:
        ##Modificar esto para guardar resultados en logs
        print("Comentario ya alamacenado anteriormente: ", idPost)

def obtenerComentarios(df):
    """
        Funciona para guardar los comentarios de facebook
        Args:
            df (string): dataset de comenarios obtenido de facebook
        return: 
            string: almacenamiento de comentarios
    """
    for i in df.index:
        print("Guardando Archivo...")
        guardarComentarioFirebase(df['comentario_completo'][i], 'user@Facebook.com', df['fecha_comentario'][i], df['id_pagina_post_comment'][i], df['categoriaComentario'][i], df['nombreProducto'][i], df['imagen'][i])
    return "Proceso Terminado...."
    
def main():
    """Funcion principal para almacanamiento de comentarios"""
    ##Lectura de archivo que contiene los ultimos comentarios de los post de facebook
    df = pd.read_csv('ResumenCommentsAPI/Logica/DatasetComentarios/datasetPostFacebook.csv', sep=';')
    obtenerComentarios(df)
    return 'ok'
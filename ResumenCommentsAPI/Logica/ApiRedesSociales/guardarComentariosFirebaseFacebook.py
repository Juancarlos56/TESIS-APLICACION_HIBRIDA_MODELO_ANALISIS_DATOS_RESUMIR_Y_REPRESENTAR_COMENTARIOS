import requests
import json
import time 
import pandas as pd
from datetime import datetime
from django.utils import timezone
from ResumenCommentsAPI.Logica.ResourcesFilesTransformerSpanish.Summarization import SummarizationPredict
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
import dateutil.parser as dateparser
from ...ClavesPrivadas.FacebookAPI import TOKEN_RAPID_API

def obtenerTipoComentario(comentario):
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
    
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'idPost', u'==', idPost).stream()
    verificacion = next(docs, None)

    if(verificacion == None):
        tipoComentario = obtenerTipoComentario(comentario)
        ##Llamada directa metodos almacenamiento API
        resumen_Comentario = SummarizationPredict().predictSummarization(comentario)
        #Almacenamiento en la base de datos en la nube
        data = {"correo_comentario":correo,"comentario_completo": comentario, 
                "tipo_comentario":tipoComentario, "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": dateparser.parse(fecha),
                "idPost": idPost,
                "RedSocial":"Facebook", 
                'categoriaComentario': categoriaComentario,  
                'nombreProducto': nombreProducto, 
                'imagen': imagen
                }
        CLOUD_DATABASE.collection("Comentario").document(idPost).set(data)
        ##Esto debido a que la api de clasificacion realiza 3 consultas por minuto, en el plan sin costo 
        time.sleep(25)
        print("Archivo Guardado :) ")
    else:
        print("Comenatarios ya alamacenado: ", idPost)

def obtenerCometarios(df):
    for i in df.index:
        print("Guardando Archivo...")
        guardarComentarioFirebase(df['comentario_completo'][i], 'user@Facebook.com', df['fecha_comentario'][i], df['id_pagina_post_comment'][i], df['categoriaComentario'][i], df['nombreProducto'][i], df['imagen'][i])
    return "Proceso Terminado...."
    
def main():
    df = pd.read_csv('ResumenCommentsAPI/Logica/DatasetComentarios/datasetPostFacebook.csv', sep=';')
    obtenerCometarios(df)
    return 'ok'
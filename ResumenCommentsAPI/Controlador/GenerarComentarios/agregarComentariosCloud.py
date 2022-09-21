from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
import pandas as pd
from ..Preprocesamiento.limpiezaData import procesamientoLimpieza
from ..loadCloudFirebase.uploadFiles import subirArchivosStorage
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone


'''
Este documento fue creado para cargar comentarios a firebase para realizar pruebas 
este documento lee un archivo csv con los comentarios proporcionados y 
va agregando mas informacion para poder realizar pruebas 
si se desea utilizar tener en cuenta que la base de datos ha cambiado por lo que 
deberia de ver cuales son los nuevos atributos que se necesitan para agregar
estos comentarios de manera rapida, Recordar esto son solo de prueba 
Si se suben todos estos comentarios recuerde que las consultas seran mas pesadas 
por la cantidad de comentarios. 
'''


#-------------------------------------------Carga comentarios dentro de cloud------------------------
def cargaDataSet(nombreArchivo):
    dataset = pd.read_csv(nombreArchivo, low_memory=False,  encoding= 'utf-8', sep=',')
    dataset = dataset.drop(['Unnamed: 0'], axis=1)
    return dataset

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def cargarComenariosFirebase(request): 
    dataset = cargaDataSet('ResumenCommentsAPI\Logica\DatasetComentarios\ComentariosConResumenCorto.csv')
    print(dataset)
    #CLOUD_DATABASE.collection("Comentario").document().set(data)
    #data = pd.DataFrame()
    #for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
    #    data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    lista = ['jbarrerab1@est.ups.edu.ec', 'katerinbarrera21@gmail.com', 
            'barrerajuan930@gmail.com', 'kbarrerab1@est.ups.edu.ec', 
            'juanperez21@gmail.com', 'christianbarrera108@gmail.com']
    
    tipo_comentario = ['very positive', 'positive', 'mixed']
    tipo_comentarioNegativo = ['negative', 'very negative']
    
    listaComentarios = []
    contPositivos = 0
    contNegativos = 0
    contUser = 0
    for i in dataset.index: 
        if(contUser >= 6):contUser = 0
        
        if(dataset["sentimiento"][i] == 1):
            if(contPositivos >= 3):contPositivos = 0

            data = {"correo_comentario":lista[contUser],"comentario_completo": dataset["Text"][i], 
                    "tipo_comentario":tipo_comentario[contPositivos], "resumen_comentario":dataset["Summary"][i], 
                    "fecha_comentario": datetime.now(tz=timezone.utc)}
            contPositivos = contPositivos + 1

        if(dataset["sentimiento"][i] == 0):
            if(contNegativos >= 2):contNegativos = 0
            data = {"correo_comentario":lista[contUser],"comentario_completo": dataset["Text"][i], 
                    "tipo_comentario":tipo_comentarioNegativo[contNegativos], "resumen_comentario":dataset["Summary"][i], 
                    "fecha_comentario": datetime.now(tz=timezone.utc)}
        
            contNegativos = contNegativos + 1 
        
        listaComentarios.append(data)
        contUser = contUser + 1
    
    for comentarios in listaComentarios:
        CLOUD_DATABASE.collection("Comentario").document().set(comentarios)
    
    return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
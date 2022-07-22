from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from datetime import datetime
from django.utils import timezone
from ..ResumenComentarios.resumenComentarios import resumenComentario as resumenComentario
import pandas as pd
from ..Preprocesamiento.limpiezaData import procesamientoLimpieza
from .metodosParaRepresentacion import (usuariosByGenero, 
                                    sentimientoDeComentario,
                                    usuariosPorEdades,obtener_top_n_words,
                                    comentariosAtravesTiempo, generandoTopicDatasetComentarios
                                    )
from django.http import JsonResponse


#-------------------------------------------Barra Horizontal para genero usuarios------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def personasPorGenero(request): 
    docs = CLOUD_DATABASE.collection(u'users').stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        usuariosCount = usuariosByGenero(data)
        return Response(usuariosCount, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------Cantidad De Comentarios por Tipo --------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def cantidadDeComentariosPorTipo(request): 
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        sentimientoCount = sentimientoDeComentario(data)
        return Response(sentimientoCount, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



##-------------------------------Comentarios a traves del tiempo con sentimientos 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def cantidadDeComentariosPorTipoSentimientoEnTiempo(request): 
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'fecha_comentario', u'>=', inicioFecha)
    docs = docs.where(u'fecha_comentario', u'<=', finFecha).stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        sentimientoCount = comentariosAtravesTiempo(data)
        return Response(sentimientoCount, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#----------------------------Topics de dataset
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def generandoTopicDataset(request): 
    topic = request.data.get('tipoDocumento')
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        valores = generandoTopicDatasetComentarios(data, topic)
        return Response(valores, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   


#-------------------------------------------Barra Vertical para edades usuarios------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def personasPorEdad(request): 
    docs = CLOUD_DATABASE.collection(u'users').stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        edades = usuariosPorEdades(data)
        return Response(edades, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#--------------------------------------Ugrama - Bigram - Trigram -----------------------------------------------------

## Un n -grama es una secuencia contigua de n elementos de una muestra dada de texto o habla.

### La función CountVectorizer"convierte una colección de documentos de texto en una matriz de recuentos de tokens"
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficasNgramasPalabras(request): 
    tipo = request.data.get('analizarComentario')
    palabras = request.data.get('numeroPalabras')
    ngrama = request.data.get('numeroNgrama')
    clasificacion = request.data.get('clasificacionComment')
    if(clasificacion == 'SinClasificacion'):
        docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    elif(clasificacion!=''):
        docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', clasificacion).stream()
        
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    
    try:      
        if(tipo == 'comentario'):
            tipoData = 'token_text'
        elif(tipo == 'resumen'): 
            tipoData = 'token_summary'
        else:
            return Response({'status':'Error Tipo comenatario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
        data = procesamientoLimpieza(data)
        top_palabras = obtener_top_n_words(data,tipoData, ngrama, palabras)
        
        return Response(top_palabras, status=status.HTTP_200_OK)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#---------------------------------lista de Comentarios para consultas basicas----------------------------


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listaComentariosUsuario(request):
    correo = request.data.get('correoComentario')  
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'correo_comentario', u'==', correo).order_by("fecha_comentario", 'DESCENDING').stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listaComentariosFechaEspecifica(request):
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'fecha_comentario', u'>=', inicioFecha).where(u'fecha_comentario', u'<=', finFecha).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listarComentarioSentimiento(request):
    tipoSentimiento = request.data.get('sentimiento')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipoSentimiento).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listarComentarioSentimientoFecha(request):
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    tipoSentimiento = request.data.get('sentimiento')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipoSentimiento)
    docs = docs.where(u'fecha_comentario', u'>=', inicioFecha)
    docs = docs.where(u'fecha_comentario', u'<=', finFecha).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 


#---------------------------------lista de Comentarios almacenados con firestorage  para consultas basicas----------------------------


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def crearContenedorDeArchivosDesarrolloPandas(request):
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    ruta = almacenamientoFileSystemDataFrame(data)
    print(ruta)
    return Response({'status':ruta}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def crearContenedorDeArchivosDesarrolloJson(request):
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    ruta = almacenamientoFileSystemJson(listData)
    print(ruta)
    return Response({'status':ruta}, status=status.HTTP_200_OK)

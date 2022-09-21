from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from datetime import datetime
from ..ResumenComentarios.resumenComentarios import resumenComentario as resumenComentario
import pandas as pd
from ..Preprocesamiento.limpiezaData import procesamientoLimpieza
from .metodosParaRepresentacion import (usuariosByGenero, 
                                    sentimientoDeComentario,
                                    usuariosPorEdades,obtener_top_n_words,
                                    comentariosAtravesTiempo, generandoTopicDatasetComentarios
                                    )
from django.http import JsonResponse

#-------------------------------------------Genero usuarios------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def personasPorGenero(request): 
    """
        REST para obtener la cantidad de usuarios por genero tiene la aplicacion
        Args:
            None: Metodo GET
        return: 
            usuariosCount(dataframe): data con la informacion de cada tipo de usuario, hombre, mujer y lgbt
    """
    ##Obteniendo coleccion de firebase respecto a usuarios
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
    """
        REST para obtener la cantidad de comentarios de nuestra aplicacion
        Args:
            None: Metodo GET
        return: 
            sentimientoCount(dataframe): data con la informacion de cada tipo de comentario con su cantidad cada uno
    """
    ##Obteniendo coleccion de firebase respecto a comentarios
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
    """
        REST para obtener la cantidad de comentarios a traves del tiempo con su respectivo sentimiento
        Args:
            fechaInicio(string): formato YYYY-mm-dd HH:mm:ss 
            fechaFin(string): formato YYYY-mm-dd HH:mm:ss
        return: 
            sentimientoCount(dataframe): data con la informacion de cada tipo de comentario con su cantidad cada uno en la fecha especifica
    """
    ##Obteniendo post y convirtiendo a datetime
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    ##Consulta utilizando firebase
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


#----------------------------Topics de dataset---------------------------------------
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def generandoTopicDataset(request): 
    """
        REST para obtener los temas que mas se tratan dentro de los comentarios 
        Args:
            tipoDocumento(string): puede ser de los comentarios o resumen
        return: 
            valores(dataframe): data con los topicos mas nombrados dentro de los comentarios 
    """
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
    """
        REST para obtener los el rango con la cantidad de personas dependiendo de la edad
        Args:
            None: Metodo GET
        return: 
            edades(dataframe): data con los rangos y cantidad de personas en ellas
    """
    ##Utilizando coleccion de firebase de usuarios
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
    """
        REST para obtener ngramas de un conjunto de texto
        Args:
            analizarComentario(string): puede ser de los comentarios o resumen
            numeroPalabras(int): cuantas palabras desea obtener, por defecto 10
            numeroNgrama(int): ugrama, bigrama, trigrama, .... (1,2,3)
            clasificacionComment(string): puede ser de los very positive, positive, ...
        return: 
            top_palabras(dataframe): data con los b-gramas que mas aparecen en el texto
    """
    tipo = request.data.get('analizarComentario')
    palabras = request.data.get('numeroPalabras')
    ngrama = request.data.get('numeroNgrama')
    clasificacion = request.data.get('clasificacionComment')
    ##Verificacion si se desea trabajar los comenatarios con clasificacion
    if(clasificacion == 'SinClasificacion'):
        docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    elif(clasificacion!=''):
        docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', clasificacion).stream()
        
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:      
        ##Verificando con que tipo trabajar si con resumenes o comentarios completos 
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
    """
        REST para obtener los comentarios de un usuarios en especifico ordenamiento desendiente
        Args:
            correoComentario(string): correo del usuario para obtener sus comentarios
        return: 
            listData(list): lista de comentarios del usuario
    """
    correo = request.data.get('correoComentario')  
    ##Ordenando de comentarios mas nuevo hasta el mas antiguo
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'correo_comentario', u'==', correo).order_by("fecha_comentario", 'DESCENDING').stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listaComentariosFechaEspecifica(request):
    """
        REST para obtener los comentarios de dentro de una fecha en especifico
        Args:
            fechaInicio(string): formato YYYY-mm-dd HH:mm:ss 
            fechaFin(string): formato YYYY-mm-dd HH:mm:ss
        return: 
            listData(list): lista de comentarios dentro de una fecha en especifico
    """
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
    """
        REST para obtener los comentarios segun un sentimiento en especifico
        Args:
            sentimiento(string): puede ser very positive, positive, mixed, negative, very negative
        return: 
            listData(list): lista de comentarios segun su tipo de sentimiento
    """
    tipoSentimiento = request.data.get('sentimiento')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipoSentimiento).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def listarComentarioSentimientoFecha(request):
    """
        REST para obtener los comentarios de dentro de una fecha y sentimiento en especifico
        Args:
            fechaInicio(string): formato YYYY-mm-dd HH:mm:ss 
            fechaFin(string): formato YYYY-mm-dd HH:mm:ss
            sentimiento(string): puede ser very positive, positive, mixed, negative, very negative
        return: 
            listData(list): lista de comentarios dentro de una fecha y sentimiento en especifico
    """
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    tipoSentimiento = request.data.get('sentimiento')
    ##Realizando Query para obtener nuestra consulta respecto a sentimiento y fechas
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipoSentimiento)
    docs = docs.where(u'fecha_comentario', u'>=', inicioFecha)
    docs = docs.where(u'fecha_comentario', u'<=', finFecha).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"comentarios": listData}) 
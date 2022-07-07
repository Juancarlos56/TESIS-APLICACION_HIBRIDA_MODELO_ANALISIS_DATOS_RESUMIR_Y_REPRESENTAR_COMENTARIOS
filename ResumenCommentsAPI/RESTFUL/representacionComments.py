from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from datetime import datetime
from django.utils import timezone
from .resumenComentarios import resumenComentario as resumenComentario
import pandas as pd
from .limpiezaData import procesamientoLimpieza
from .metodosRepresentacion import (nubePalabras, usuariosByGenero, 
                                    graficaDeSentimientoComentario,
                                    graficaPorEdades,obtener_top_n_words
                                    )
from .uploadFiles import subirArchivosStorage

#---------------------------------Nube de palabras para comentario Completo
##Nube palabras comentario completo
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantes(request): 
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try: 
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_text, "topPalabrasMasImportantesComentario")
        pathCloud = 'images/nubePalabras/topPalabrasMasImportantesComentario.png'
        rutaPath = subirArchivosStorage(pathIMG,pathCloud)

        return Response({'status':rutaPath}, status=status.HTTP_200_OK)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



##Nube de palabras para tipo de comentario completo
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantesByTipo(request, tipo): 
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipo).stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_text, "topPalabrasMasImportantesComentarioBy-"+tipo)
        pathCloud="images/nubePalabras/topPalabrasMasImportantesComentarioBy-"+tipo+'.png'
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantesByRangoFecha(request): 
    inicioFecha = datetime.strptime(request.data.get('inicioFecha'), '%Y/%m/%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('finFecha'), '%Y/%m/%d %H:%M:%S')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'fecha_comentario', u'>=', inicioFecha).where(u'fecha_comentario', u'<=', finFecha).stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_text, "topPalabrasMasImportantesComentarioRangoFecha")
        pathCloud="images/nubePalabras/topPalabrasMasImportantesComentarioRangoFecha.png"
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

##-----------------------Nube de palabras para resumen ---------------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantesResumen(request): 
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try: 
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_summary, "topPalabrasMasImportantesResumen")
        pathCloud = 'images/nubePalabras/topPalabrasMasImportantesResumen.png'
        rutaPath = subirArchivosStorage(pathIMG,pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_200_OK)
    except:
        return Response({'status':'Erro generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantesResumenByTipo(request, tipo): 
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', tipo).stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_summary, "topPalabrasMasImportantesResumenBy-"+tipo)
        pathCloud="images/nubePalabras/topPalabrasMasImportantesResumenBy-"+tipo+'.png'
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Erro generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def topPalabrasMasImportantesResumenByRangoFecha(request): 
    inicioFecha = datetime.strptime(request.data.get('inicioFecha'), '%Y/%m/%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('finFecha'), '%Y/%m/%d %H:%M:%S')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'fecha_comentario', u'>=', inicioFecha).where(u'fecha_comentario', u'<=', finFecha).stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data = procesamientoLimpieza(data)
        pathIMG = nubePalabras(data.token_summary, "topPalabrasMasImportantesResumenRangoFecha")
        pathCloud="images/nubePalabras/topPalabrasMasImportantesResumenRangoFecha.png"
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#-------------------------------------------Histogramas para comentarios completos------------------------


#-------------------------------------------Barra Horizontal para genero usuarios------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def personasPorGenero(request): 
    docs = CLOUD_DATABASE.collection(u'users').stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        pathIMG = usuariosByGenero(data)
        pathCloud="images/generoUsers/generoUsuariosApp.png"
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Erro generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------Pie clasificacion sentimiento --------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def clasificacionSentimientosPie(request): 
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        pathIMG = graficaDeSentimientoComentario(data)
        pathCloud="images/clasificacionSentimiento/sentimientoComentarioPie.png"
        rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status':'Erro generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#-------------------------------------------Barra Vertical para edades usuarios------------------------

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def personasPorEdad(request): 
    docs = CLOUD_DATABASE.collection(u'users').stream()
    data = pd.DataFrame()
    for doc in docs:
        #data = data.append(doc.to_dict(), ignore_index=True)
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    try:
        data.reset_index(drop=True, inplace=True)
        pathIMG = graficaPorEdades(data)
        pathCloud="images/edades/edadesUsuariosApp.png"
        #rutaPath = subirArchivosStorage(pathIMG, pathCloud)
        return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
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
        pathIMG = obtener_top_n_words(data,tipoData, ngrama, palabras)
        pathCloud = 'images/ngrmas/ugramas-'+tipo+'-'+str(clasificacion.replace(" ", ""))+'-'+str(ngrama)+'grama.png'
        rutaPath = subirArchivosStorage(pathIMG,pathCloud)
        return Response({'status':rutaPath}, status=status.HTTP_200_OK)
    except:
        return Response({'status':'Error generando grafico y storage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

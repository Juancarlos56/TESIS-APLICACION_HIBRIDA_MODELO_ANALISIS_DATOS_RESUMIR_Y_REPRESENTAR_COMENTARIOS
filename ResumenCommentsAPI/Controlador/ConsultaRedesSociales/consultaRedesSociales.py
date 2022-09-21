from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.Logica.ApiRedesSociales.obtenerComenariosAPI_Facebook import main as obtenerComentariosFacebook
from ResumenCommentsAPI.Logica.ApiRedesSociales.guardarComentariosFirebaseFacebook import main as almacenarComentariosFacebook
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from django.http import JsonResponse
from datetime import datetime

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def obtenerComentariosUltimas25Publicaciones(request): 
    """
        REST para obtencion de las ultimas 25 publicaciones de facebook
        cuando se llema a este metodo se actualiza el archivo csv con 
        las publicaciones de facebook: ResumenCommentsAPI\Logica\DatasetComentarios\datasetPostFacebook.csv.
        Args:
            none: Metodo GET
        return: 
            dataframe: dataset con las 25 publicaciones de facebook
    """
    df = obtenerComentariosFacebook()
    return Response(df, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def almacenarComentariosUltimas25Publicaciones(request): 
    """
        REST para almacenamiento de las ultimas 25 publicaciones de facebook dentro de firebase
        Args:
            none: Metodo GET
        return: 
            status: si no existe ningun error al almacenar los comentarios se retorna: 'ok' o sino: 'error'
    """
    try:
        respuesta = almacenarComentariosFacebook()
        return Response({'status':respuesta}, status=status.HTTP_200_OK)
    except:
        return Response({'status':'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def filtrarComentariosRedesSociales(request): 
    """
        REST para buscar informacion dentro de los comentarios de facebook por fecha de inicio y fin
        Args:
            fechaInicio(string): formato 2022-08-20 16:00:00
            fechaFin(string): formato 2022-09-20 16:00:00
        return: 
            list: Listado de los comentarios filtrados.
    """
    ##Convirtiendo fecha inicio y fin de string a datetime
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    ##Busqueda de comentarios almacenados en firebase por tipo de red social 'facebook'
    ##En donde se busca segun la fecha del comentario
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'RedSocial', u'==', 'Facebook').where(u'fecha_comentario', u'>=', inicioFecha).where(u'fecha_comentario', u'<=', finFecha).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"ComentariosRedesSociales": listData}) 

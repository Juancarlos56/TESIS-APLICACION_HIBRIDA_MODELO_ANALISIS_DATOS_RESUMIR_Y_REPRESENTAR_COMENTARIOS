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
    df = obtenerComentariosFacebook()
    return Response(df, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def almacenarComentariosUltimas25Publicaciones(request): 
    #try:
    respuesta = almacenarComentariosFacebook()
    return Response({'status':respuesta}, status=status.HTTP_200_OK)
    #except:
    #    return Response({'status':'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def filtrarComentariosRedesSociales(request): 
    inicioFecha = datetime.strptime(request.data.get('fechaInicio'), '%Y-%m-%d %H:%M:%S')
    finFecha = datetime.strptime(request.data.get('fechaFin'), '%Y-%m-%d %H:%M:%S')
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'RedSocial', u'==', 'Facebook').where(u'fecha_comentario', u'>=', inicioFecha).where(u'fecha_comentario', u'<=', finFecha).stream()
    listData = []
    for doc in docs:
        listData.append(doc.to_dict())
    return JsonResponse({"ComentariosRedesSociales": listData}) 

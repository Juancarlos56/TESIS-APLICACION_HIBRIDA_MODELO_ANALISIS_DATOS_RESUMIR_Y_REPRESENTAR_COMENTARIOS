from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.Logica.ApiRedesSociales.obtenerComenariosAPI_Facebook import main as obtenerComentariosFacebook
from ResumenCommentsAPI.Logica.ApiRedesSociales.guardarComentariosFirebaseFacebook import main as almacenarComentariosFacebook


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def obtenerComentariosUltimas25Publicaciones(request): 
    tokenApi = request.data.get('tokenApi')
    
    df = obtenerComentariosFacebook(tokenApi)
    return Response(df, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def almacenarComentariosUltimas25Publicaciones(request): 
    #try:
    respuesta = almacenarComentariosFacebook()
    return Response({'status':respuesta}, status=status.HTTP_200_OK)
    #except:
    #    return Response({'status':'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
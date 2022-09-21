from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from datetime import datetime
from django.utils import timezone
from .resumenComentarios import resumenComentario as resumenComentario

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def guardarComentario(request): 
    """
        REST para almacenar un comentario sin categoria, ni producto, simplemente un comentario
        Args:
            contenido_comentario(string): Comentario completo
            tipoComentario(string): Clasificacion de comentario very positive, positive, mixed, negative, very negative
            correoComentario(string): Correo de la persona que hizo el comentario
        return: 
            boolean: true correcto almacenamiento y false no se guardo el comentario
    """
    ## Recibimos los parametros enviados desde IONIC
    contenido_comentario = request.data.get('contenido_comentario')
    tipoComentario = request.data.get('tipoComentario')
    correoComentario = request.data.get('correoComentario')

    try:
        ##Llamada al metodo transformer
        resumen_Comentario = resumenComentario(contenido_comentario)
        #Almacenamiento en la base de datos en la nube
        ##Colocamos General porque aun no se definian bien los grupos para la base de datos
        data = {"correo_comentario":correoComentario,"comentario_completo": contenido_comentario, 
                "tipo_comentario":tipoComentario, "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": datetime.now(tz=timezone.utc),
                "idPost": "NOT ID",
                "RedSocial":"COCOments", 
                "categoriaComentario": 'General',  
                "nombreProducto": "General",
                "imagen":"notImagen"}
    
        #IDS generados automaticamente por firebase, para modificar agregar un valor dentro de document
        CLOUD_DATABASE.collection("Comentario").document().set(data)
        return Response({'stateComment': 'True'}, status=status.HTTP_201_CREATED)
    except:
        return Response({'stateComment': 'False'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def guardarComentarioClasificacion(request): 
    """
        REST para almacenar un comentario segun el servicio al que pertenece: limpieza, comida, ubicacion
        Args:
            contenido_comentario(string): Comentario completo
            tipoComentario(string): Clasificacion de comentario very positive, positive, mixed, negative, very negative
            correoComentario(string): Correo de la persona que hizo el comentario
            categoriaComentario(string): Servicio al que pertence el comentario, limpieza, comida, ubicacion, .... ver en firebase
        return: 
            boolean: true correcto almacenamiento y false no se guardo el comentario
    """
    contenido_comentario = request.data.get('contenido_comentario')
    tipoComentario = request.data.get('tipoComentario')
    correoComentario = request.data.get('correoComentario')
    categoriaComentario = request.data.get('categoriaComentario')

    try:
        resumen_Comentario = resumenComentario(contenido_comentario)
        #Almacenamiento en la base de datos en la nube
        data = {"correo_comentario":correoComentario,"comentario_completo": contenido_comentario, 
                "tipo_comentario":tipoComentario, "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": datetime.now(tz=timezone.utc),
                "idPost": "NOT ID",
                "RedSocial":"COCOments", 
                "categoriaComentario": categoriaComentario,  
                "nombreProducto": "General",
                "imagen":"notImagen"}
    
        #IDS generados automaticamente por firebase, para modificar agregar un valor dentro de document
        CLOUD_DATABASE.collection("Comentario").document().set(data)
        return Response({'stateComment': 'True'}, status=status.HTTP_201_CREATED)
    except:
        return Response({'stateComment': 'False'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def guardarComentarioClasificacionProducto(request): 
    """
        REST para almacenar un comentario segun el servicio de comida, ademas del plato al que se realiza el comentario
        Parameters:
            contenido_comentario(string): Comentario completo
            tipoComentario(string): Clasificacion de comentario very positive, positive, mixed, negative, very negative
            correoComentario(string): Correo de la persona que hizo el comentario
            categoriaComentario(string): Servicio al que pertence el comentario, limpieza, comida, ubicacion, .... ver en firebase
            nombreProducto(string): Este atributo hace referencia al nombre del plato de comida, ya que solo este servicio se encuentra con productos actualmente
        Responses: 
            boolean: true correcto almacenamiento y false no se guardo el comentario
    """
    contenido_comentario = request.data.get('contenido_comentario')
    tipoComentario = request.data.get('tipoComentario')
    correoComentario = request.data.get('correoComentario')
    categoriaComentario = request.data.get('categoriaComentario')
    nombreProducto = request.data.get('nombreProducto')

    try:
        resumen_Comentario = resumenComentario(contenido_comentario)
        #Almacenamiento en la base de datos en la nube
        data = {"correo_comentario":correoComentario,"comentario_completo": contenido_comentario, 
                "tipo_comentario":tipoComentario, "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": datetime.now(tz=timezone.utc),
                "idPost": "NOT_ID",
                "RedSocial":"COCOments", 
                "categoriaComentario": categoriaComentario,  
                "nombreProducto": nombreProducto,
                "imagen":"notImagen"
                }
    
        #IDS generados automaticamente por firebase, para modificar agregar un valor dentro de document
        CLOUD_DATABASE.collection("Comentario").document().set(data)
        return Response({'stateComment': 'True'}, status=status.HTTP_201_CREATED)
    except:
        return Response({'stateComment': 'False'}, status=status.HTTP_201_CREATED)
    
    
    
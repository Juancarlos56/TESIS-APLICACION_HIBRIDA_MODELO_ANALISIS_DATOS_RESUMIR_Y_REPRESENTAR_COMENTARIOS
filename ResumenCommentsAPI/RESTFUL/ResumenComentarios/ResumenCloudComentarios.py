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
    ## Recibimos los parametros enviados desde IONIC
    ## contenido_comentario = Comentario completo
    ## tipoComentario = Clasificacion de comentario bueno, malo, neutral
    ## correoComentario = Correo de la persona que hizo el comentario
    contenido_comentario = request.data.get('contenido_comentario')
    tipoComentario = request.data.get('tipoComentario')
    correoComentario = request.data.get('correoComentario')

    try:
        resumen_Comentario = resumenComentario(contenido_comentario)
        #Almacenamiento en la base de datos en la nube
        data = {"correo_comentario":correoComentario,"comentario_completo": contenido_comentario, 
                "tipo_comentario":tipoComentario, "resumen_comentario":resumen_Comentario, 
                "fecha_comentario": datetime.now(tz=timezone.utc),
                "idPost": "NOT ID",
                "RedSocial":"COCOments"}
    
        #IDS generados automaticamente por firebase, para modificar agregar un valor dentro de document
        CLOUD_DATABASE.collection("Comentario").document().set(data)
        return Response({'stateComment': 'True'}, status=status.HTTP_201_CREATED)
    except:
        return Response({'stateComment': 'False'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def guardarComentarioClasificacion(request): 
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
    
    
    
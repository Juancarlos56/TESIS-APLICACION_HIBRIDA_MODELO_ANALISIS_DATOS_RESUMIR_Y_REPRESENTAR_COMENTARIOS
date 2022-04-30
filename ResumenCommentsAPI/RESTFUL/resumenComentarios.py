from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


#@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def resumenComentario(comentarioCompleto):
    return "algoritmo para resumen de texto"
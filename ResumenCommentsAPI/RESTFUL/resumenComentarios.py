from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from ResumenCommentsAPI.Logica.ResourcesFilesTransformerSpanish.Summarization import SummarizationPredict

"""
    Metodo que conecta con el servicio para resumen de texto
    recibimos el texto ingresado por el usuario
    model transformer es el encargado de realizar el resumen
"""
def resumenComentario(comentarioCompleto):
    return SummarizationPredict().predictSummarization(comentarioCompleto)
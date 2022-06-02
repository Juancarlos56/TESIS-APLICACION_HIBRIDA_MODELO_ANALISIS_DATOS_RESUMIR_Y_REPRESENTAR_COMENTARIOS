from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from django.shortcuts import render
from ResumenCommentsAPI.Logica import modelo #para utilizar el método inteligente

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse


class Regresion():
    def mostrarFormulario(request):
        return render(request, "inicio.html")
    @api_view(['GET','POST'])
    @permission_classes((permissions.AllowAny,))

    def predecir(request):
        try:
            #Formato de datos de entrada
            Edad = int(request.POST.get('Edad'))
            print(Edad)
            
            #Consumo de la lógica para predecir si se aprueba o no el crédito
            resul=modelo.modelo.predecir(modelo.modelo,Edad=Edad)
        except:
            resul='Datos inválidos'
        return render(request, "resultado.html",{"e":resul})

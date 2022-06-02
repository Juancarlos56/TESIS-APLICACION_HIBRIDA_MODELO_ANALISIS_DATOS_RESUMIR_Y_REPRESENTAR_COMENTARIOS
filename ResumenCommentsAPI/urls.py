from django.urls import include, path
from django.urls import re_path as url
from rest_framework import routers
from ResumenCommentsAPI import views as views 
from ResumenCommentsAPI.RESTFUL import clasificacionComentarios as clasificacionComentarios  


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/guardarCometario$', clasificacionComentarios.guardarComentario),
    url(r'home',views.Regresion.mostrarFormulario),
    url(r'predecir/',views.Regresion.predecir),


]
from django.urls import include, path
from django.urls import re_path as url
from rest_framework import routers
from ResumenCommentsAPI.RESTFUL import clasificacionComentarios as clasificacionComentarios  

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/guardarCometario$', clasificacionComentarios.guardarComentario),
]
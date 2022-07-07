from django.urls import include, path
from django.urls import re_path as url
from rest_framework import routers
from ResumenCommentsAPI import views as views 
from ResumenCommentsAPI.RESTFUL import clasificacionComentarios as clasificacionComentarios  
from ResumenCommentsAPI.RESTFUL import representacionComments as representacionComments  


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/guardarComentario$', clasificacionComentarios.guardarComentario),
    #Nube de palabras para comentario
    path('api/topPalabrasComentario/<str:tipo>', representacionComments.topPalabrasMasImportantesByTipo),
    path('api/topPalabrasComentario', representacionComments.topPalabrasMasImportantes),
    url(r'^api/topPalabrasComentarioRangoFechas$', representacionComments.topPalabrasMasImportantesByRangoFecha),
    #Nube de palabras para Resumen
    path('api/topPalabrasResumen/<str:tipo>', representacionComments.topPalabrasMasImportantesResumenByTipo),
    path('api/topPalabrasResumen', representacionComments.topPalabrasMasImportantesResumen),
    url(r'^api/topPalabrasResumenRangoFechas$', representacionComments.topPalabrasMasImportantesResumenByRangoFecha),
    #Grafica de genero usuarios
    path('api/usersGenero', representacionComments.personasPorGenero),
    #Grafica de pie de sentimiento comments 
    path('api/clasificacionSentimientosPie', representacionComments.clasificacionSentimientosPie),
    #Grafica de edad usuarios
    path('api/usersEdad', representacionComments.personasPorEdad),
    #Top palabras mas usadas
    url(r'^api/graficasNgramasPalabras$', representacionComments.graficasNgramasPalabras),
    
    #url(r'home',views.Regresion.mostrarFormulario),
    #url(r'predecir/',views.Regresion.predecir),


]
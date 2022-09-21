from django.urls import include, path
from django.urls import re_path as url
from rest_framework import routers
from ResumenCommentsAPI import views as views 
from ResumenCommentsAPI.Controlador.ResumenComentarios import ResumenCloudComentarios as ResumenCloudComentarios  
from ResumenCommentsAPI.Controlador.GeneracionGraficasPython import representacionCommentsGraficas as representacionCommentsGraficas
from ResumenCommentsAPI.Controlador.ConsultasGeneralesDataSet import representacionComments as representacionComments  
from ResumenCommentsAPI.Controlador.GenerarComentarios import agregarComentariosCloud as agregarComentariosCloud
from ResumenCommentsAPI.Controlador.ConsultasRestaurante import consultaRestaurante as consultaRestaurante
from ResumenCommentsAPI.Controlador.ConsultaRedesSociales import consultaRedesSociales as consultaRedesSociales

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #Almacenamiento de comentarios
    url(r'^api/guardarComentario$', ResumenCloudComentarios.guardarComentario),
    url(r'^api/guardarComentarioClasificacion$', ResumenCloudComentarios.guardarComentarioClasificacion),
    url(r'^api/guardarComentarioClasificacionProducto$', ResumenCloudComentarios.guardarComentarioClasificacionProducto),
    
    #Nube de palabras para comentario
    path('api/topPalabrasComentario/<str:tipo>', representacionCommentsGraficas.topPalabrasMasImportantesByTipo),
    path('api/topPalabrasComentario', representacionCommentsGraficas.topPalabrasMasImportantes),
    url(r'^api/topPalabrasComentarioRangoFechas$', representacionCommentsGraficas.topPalabrasMasImportantesByRangoFecha),
    
    #Nube de palabras para Resumen
    path('api/topPalabrasResumen/<str:tipo>', representacionCommentsGraficas.topPalabrasMasImportantesResumenByTipo),
    path('api/topPalabrasResumen', representacionCommentsGraficas.topPalabrasMasImportantesResumen),
    url(r'^api/topPalabrasResumenRangoFechas$', representacionCommentsGraficas.topPalabrasMasImportantesResumenByRangoFecha),
    
    #-------------------URLS pensadas para el negocio -------------------
    #Top Platos malos 

    #Top palabras mas usadas
    url(r'^api/graficasNgramasPalabras$', representacionComments.graficasNgramasPalabras),
    
    #Topic de palabras segun documento de comentarios
    url(r'^api/generandoTopicDataset', representacionComments.generandoTopicDataset),
    
    #Buscar palabras por categoria
    url(r'^api/buscarCategoriaComentario$', consultaRestaurante.buscarCategoriaComentario),
    
    #Buscar palabras en especifico
    url(r'^api/buscarEnDataset$', consultaRestaurante.buscarEnDataset),
    
    #Grafica de genero usuarios
    path('api/usersGenero', representacionComments.personasPorGenero),
    
    #Cantidad de comentarios por tipo
    path('api/cantidadDeComentariosPorTipo', representacionComments.cantidadDeComentariosPorTipo),
    
    #Grafica de edad usuarios
    path('api/usersEdad', representacionComments.personasPorEdad),
    
    ##Retorno de lista de comentarios de un usuario
    url(r'^api/comentariosUsuario$', representacionComments.listaComentariosUsuario),
    
    ##Retorno de lista de comentarios por fecha
    url(r'^api/listarComentarioFecha$', representacionComments.listaComentariosFechaEspecifica),
    
    ##Retorno de lista de comentarios por sentimiento
    url(r'^api/listarComentarioSentimiento$', representacionComments.listarComentarioSentimiento),
    
    ##Retorno de lista de comentarios por sentimiento y fecha
    url(r'^api/listarComentarioSentimientoFecha$', representacionComments.listarComentarioSentimientoFecha),
    
    #Cantidad de comentarios por tipo sentimiento en el tiempo
    url(r'^api/cantidadDeComentariosPorTipoSentimientoEnTiempo', representacionComments.cantidadDeComentariosPorTipoSentimientoEnTiempo),
    
    ##------------------------Redes Sociales---------------------
    ##Obtener ultimas 25 publicaciones de facebook
    path('api/obtenerComentariosFacebook', consultaRedesSociales.obtenerComentariosUltimas25Publicaciones),
    
    ##Guardar ultimas 25 publicaciones de facebook
    path('api/guardarComentariosFacebook', consultaRedesSociales.almacenarComentariosUltimas25Publicaciones),
    
    ##Obtener ultimas 25 publicaciones de facebook
    url(r'^api/filtrarComentariosFacebookFecha', consultaRedesSociales.filtrarComentariosRedesSociales),
    
    ##------------------------Mejores platos de restaurante-----------------------------
    
    ##Obtener los 3 mejores y peores platos del restaurante
    path('api/obtenerMejoresPeoresPlatosRestaurantes',consultaRestaurante.obtenerMejoresPeoresPlatosRestaurantes),
    
    #----------------URLS para interfaz grafica django----------------------
    #url(r'home',views.Regresion.mostrarFormulario),
    #url(r'predecir/',views.Regresion.predecir),

]
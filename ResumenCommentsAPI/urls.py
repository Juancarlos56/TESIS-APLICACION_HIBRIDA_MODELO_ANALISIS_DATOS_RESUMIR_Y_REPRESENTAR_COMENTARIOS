from django.urls import include, path
from django.urls import re_path as url
from rest_framework import routers
from ResumenCommentsAPI import views as views 
from ResumenCommentsAPI.RESTFUL.ResumenComentarios import ResumenCloudComentarios as ResumenCloudComentarios  
from ResumenCommentsAPI.RESTFUL.GeneracionGraficasPython import representacionCommentsGraficas as representacionCommentsGraficas
from ResumenCommentsAPI.RESTFUL.ConsultasGeneralesDataSet import representacionComments as representacionComments  
from ResumenCommentsAPI.RESTFUL.GenerarComenatarios import agregarComentariosCloud as agregarComentariosCloud
from ResumenCommentsAPI.RESTFUL.ConsultasRestaurante import consultaRestaurante as consultaRestaurante
from ResumenCommentsAPI.RESTFUL.ConsultaRedesSociales import consultaRedesSociales as consultaRedesSociales

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/guardarComentario$', ResumenCloudComentarios.guardarComentario),
    #Nube de palabras para comentario
    path('api/topPalabrasComentario/<str:tipo>', representacionCommentsGraficas.topPalabrasMasImportantesByTipo),
    path('api/topPalabrasComentario', representacionCommentsGraficas.topPalabrasMasImportantes),
    url(r'^api/topPalabrasComentarioRangoFechas$', representacionCommentsGraficas.topPalabrasMasImportantesByRangoFecha),
    #Nube de palabras para Resumen
    path('api/topPalabrasResumen/<str:tipo>', representacionCommentsGraficas.topPalabrasMasImportantesResumenByTipo),
    path('api/topPalabrasResumen', representacionCommentsGraficas.topPalabrasMasImportantesResumen),
    url(r'^api/topPalabrasResumenRangoFechas$', representacionCommentsGraficas.topPalabrasMasImportantesResumenByRangoFecha),
    #Top palabras mas usadas
    url(r'^api/graficasNgramasPalabras$', representacionComments.graficasNgramasPalabras),
    #Topic de palabras segun documento de comentarios
    url(r'^api/generandoTopicDataset', representacionComments.generandoTopicDataset),
    
    #--------------------------URLS para carga de datos de datatoy
    #Cargar de comentarios para analisis
    ##Descomentar Url para generar registrar nuevos comentarios
    #path('api/cargaComentarios', agregarComentariosCloud.cargarComenariosFirebase),

    ##URLS pensadas para el negocio 
    #Top Platos malos 
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
    ##Obtener ultimas 25 publicaciones de facebook
    url(r'^api/obtenerComentariosFacebook', consultaRedesSociales.obtenerComentariosUltimas25Publicaciones),
    ##Guardar ultimas 25 publicaciones de facebook
    path('api/guardarComentariosFacebook', consultaRedesSociales.almacenarComentariosUltimas25Publicaciones),
    
    #----------------URLS para interfaz grafica django----------------------
    #url(r'home',views.Regresion.mostrarFormulario),
    #url(r'predecir/',views.Regresion.predecir),


]
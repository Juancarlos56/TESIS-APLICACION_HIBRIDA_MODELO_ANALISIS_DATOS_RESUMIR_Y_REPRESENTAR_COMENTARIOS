from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ResumenCommentsAPI.ClavesPrivadas.firebaseAdminConfig import CLOUD_DATABASE
from ..ResumenComentarios.resumenComentarios import resumenComentario as resumenComentario
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from ..loadCloudFirebase.uploadFiles import subirArchivosStorage
from ..Preprocesamiento.limpiezaData import procesamientoLimpieza, lematizacion
import operator


def buscarEnDatasetPalabras(data, tipo, textoBuscar):
    """
        Funcion para buscar una palabra en especifico dentro del dataset
        Args:
            data(dataframe): dataset con comentarios 
            tipo(string): columna a la que se va a analizar, puede ser comentario completo o resumen  
            textoBuscar(string): palabra que se desea buscar.
        return: 
            numeroComentarios: cuantos comentarios contiene esa palabra
            datasetTexto: dataset de todos los comentarios con esa palabra 
            rutaImg: URL de la imagen que se almaceno dentro de firestorage
    """
    
    ##Realizamos lematizacion para nuestro texto a buscar
    texto = lematizacion(textoBuscar)
    ##Cuantos Comentarios referenciados con algun plato
    ##Trabajamos con el dataset con la columna que contiene lematizacion y buscamos 
    ##las filas que contienen nuestra palabra 
    datasetTexto = data[data.lema_text.str.contains(str(texto+'?'), regex=True, case=False)]    
    numeroComentarios =datasetTexto.lema_text.count()
    ##Si no existe ningun resultado
    if(datasetTexto.empty):
       return '0', '0','not exist'
    ##con la data, ahora trabajamos con los comentarios o resumen para generar la nube de palabras
    text = " ".join(review for review in datasetTexto[tipo])
    ##Nube de palabras con respecto data
    wc = WordCloud(width=1024, height=768, background_color="white", colormap="Dark2",max_font_size=150)
    wordcloud = wc.generate(text)
    ##Path de almacenamiento en local
    wordcloud.to_file("static/images/nubePalabras/palabrasGeneradas.png")
    ##Path de almacenamiento en la nube
    pathCloud = 'images/nubePalabras/palabrasGeneradas.png'
    rutaImg = subirArchivosStorage("static/images/nubePalabras/palabrasGeneradas.png",pathCloud)
    return numeroComentarios, datasetTexto, rutaImg
    
    

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def buscarEnDataset(request): 
    """
        REST para buscar una palabra en especifico dentro del dataset
        Args:
            analizarComentario(string): columna a la que se va a analizar, puede ser comentario completo o resumen  
            texto(string): palabra que se desea buscar.
        return: 
            numeroComentarios: cuantos comentarios contiene esa palabra
            datasetTexto: dataset de todos los comentarios con esa palabra 
            rutaImg: URL de la imagen que se almaceno dentro de firestorage
    """
    tipo = request.data.get('analizarComentario')
    texto = request.data.get('texto')
    ##Obtencion de la coleccion de comentarios
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    ##De coleccion a dataframes
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    ##Asignando tipo de analisis, segun comentario o resumen     
    if(tipo == 'comentario'):
        tipoData = 'lema_text'
    elif(tipo == 'resumen'): 
        tipoData = 'lema_summary'
    else:
        return Response({'status':'Error Tipo comentario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
    #print("**********:", data)
    ##Realizamos preprocesamieto del dataset para tener un dataset con el trabajar
    data = procesamientoLimpieza(data)
    #print(data)
    numeroComentarios, datasetTexto,rutaImg = buscarEnDatasetPalabras(data,tipoData, texto)
    return Response({ 
                    "numeroComentarios" : numeroComentarios, 
                    "comentarios": datasetTexto, 
                    "rutaImg": rutaImg
                    }, status=status.HTTP_200_OK)


def buscarEnDatasetCategorias(data, tipo):
    """
        REST para buscar por categorias dentro del dataset
        Args:
            data(dataframe): dataset con comentarios 
            tipo(string): columna a la que se va a analizar, puede ser comentario completo o resumen  
        return: 
            rutaImg: URL de la imagen que se almaceno dentro de firestorage
    """
    ##Obteniendo columna de las que se genera la imagen
    text = " ".join(review for review in data[tipo])
    wc = WordCloud(width=1024, height=768, background_color="white", colormap="Dark2",max_font_size=150)
    wordcloud = wc.generate(text)
    wordcloud.to_file("static/images/nubePalabras/palabrasGeneradas.png")
    pathCloud = 'images/nubePalabras/palabrasGeneradas.png'
    rutaImg = subirArchivosStorage("static/images/nubePalabras/palabrasGeneradas.png",pathCloud)
    return rutaImg

### La función CountVectorizer"convierte una colección de documentos de texto en una matriz de recuentos de tokens"
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def buscarCategoriaComentario(request): 
    """
        REST para buscar una palabra en especifico dentro del dataset
        Args:
            analizarComentario(string): columna a la que se va a analizar, puede ser comentario completo o resumen  
            categoria(string): tipo de categoria dependiendo de la base de datos de firebase
            clasificacionComment(string): 6 opciones: sin clasificacion, very positive, positive, mixed, negative, very negative
        return: 
            numeroComentarios: cuantos comentarios contiene esa palabra
            datasetTexto: dataset de todos los comentarios con esa palabra 
            rutaImg: URL de la imagen que se almaceno dentro de firestorage
    """
    tipo = request.data.get('analizarComentario')
    categoria = request.data.get('categoria')
    clasificacionComment = request.data.get('clasificacionComment')
    
    ##Filtrado de comentarios respecto a una categoria (general, comida, limpieza, etc------coleccion servicios)
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'categoriaComentario', u'==', categoria)
    ##si se desea analizar segun un  tipo de comentario 
    if(clasificacionComment != 'SinClasificacion'):
        docs = docs.where(u'tipo_comentario', u'==', clasificacionComment)
    
    docs = docs.stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    ##De donde se desea analizar los comentarios(completo o resumen)
    if(tipo == 'comentario'):
        tipoData = 'lema_text'
    elif(tipo == 'resumen'): 
        tipoData = 'lema_summary'
    else:
        return Response({'status':'Error Tipo comenatario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
    ##Limpeiza de data
    data = procesamientoLimpieza(data)
    rutaImg = buscarEnDatasetCategorias(data,tipoData)
    numeroComentarios = data.shape[0]
    return Response({ 
                    "numeroComentarios" : numeroComentarios, 
                    "comentarios": data, 
                    "rutaImg": rutaImg
                    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def obtenerMejoresPeoresPlatosRestaurantes(request): 
    """
        REST para buscar una palabra en especifico dentro del dataset
        Args:
            None: Metodo GET
        return: 
            mejores_productos: lista de los mejores platos del restaurate
            peores_productos: lista de los peores platos del restaurante 
    """
    ##Obteniendo coleccion de productos de firebase
    productosCollention = CLOUD_DATABASE.collection(u'Producto').stream()
    productos = pd.DataFrame()
    for doc in productosCollention:
        productos = pd.concat([productos, pd.DataFrame.from_records([doc.to_dict()])])
    
    productosComentariosPositivos = {}
    productosComentariosNegativos = {}
    ##Analizando cada producto de nuestra comida
    ##Aplicar estructuras de datos para mejorar esta consulta
    for index, row in productos.iterrows():
        nombreProducto = str(row.nombreProducto)
        ##Obteniendo comentarios positivos del producto
        ##Solo se usan very positive, si usted concidera que entrar los positive 
        ##Agregar nueva consulta con 'where' o 'or'
        docs = CLOUD_DATABASE.collection(u'Comentario').where(u'nombreProducto', u'==', nombreProducto).where(u'tipo_comentario', u'==', 'very positive').stream()
        docs2 = CLOUD_DATABASE.collection(u'Comentario').where(u'nombreProducto', u'==', nombreProducto).where(u'tipo_comentario', u'==', 'very negative').stream()
        
        ##Contamos cuantos comentarios con clasificacion de excelente tiene cada producto
        cantidadPositivos = len(list(docs))
        productosComentariosPositivos[nombreProducto]=cantidadPositivos
        ##Contamos cuantos comentarios con clasificacion de mala tiene cada producto
        cantidadNegativos = len(list(docs2))
        productosComentariosNegativos[nombreProducto]=cantidadNegativos
    
    ##Ordenamiento de comentarios de mayor a menor
    productosComentariospositivos_sort = sorted(productosComentariosPositivos.items(), key=operator.itemgetter(1), reverse=True)
    productosComentariosnegativos_sort = sorted(productosComentariosNegativos.items(), key=operator.itemgetter(1), reverse=True)
    ##Obtenemos solo los 3 mejores y 3 peores
    mejoresProductos= productosComentariospositivos_sort[:3]
    peoresProductos= productosComentariosnegativos_sort[:3]
    
    return Response({"mejores_productos": mejoresProductos, "peores_productos": peoresProductos}, status=status.HTTP_200_OK)
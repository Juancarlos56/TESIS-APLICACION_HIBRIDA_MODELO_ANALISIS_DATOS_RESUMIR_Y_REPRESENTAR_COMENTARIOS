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
    ##Nube de palabras con respecto data
    ##Pasamos nuestra columna a texto
    ##Numero de veces que sale el texto entre los comentarios 
    #numeroApariciones = data[[textoBuscar]].sort_values(by=textoBuscar).count()
    #datasetTexto =  data[data[type].str.contains(str(textoBuscar+'?'), regex=True, case=False)]
    texto = lematizacion(textoBuscar)
    ##Cuantos Comentarios referenciados con algun plato
    datasetTexto = data[data.lema_text.str.contains(str(texto+'?'), regex=True, case=False)]    
    numeroComentarios =datasetTexto.lema_text.count()
    if(datasetTexto.empty):
       return '0', '0','not exist'

    text = " ".join(review for review in datasetTexto[tipo])
    wc = WordCloud(width=1024, height=768, background_color="white", colormap="Dark2",max_font_size=150)
    wordcloud = wc.generate(text)
    wordcloud.to_file("static/images/nubePalabras/palabrasGeneradas.png")
    pathCloud = 'images/nubePalabras/palabrasGeneradas.png'
    rutaImg = subirArchivosStorage("static/images/nubePalabras/palabrasGeneradas.png",pathCloud)
    
    return numeroComentarios, datasetTexto, rutaImg
    
    
    

    

### La función CountVectorizer"convierte una colección de documentos de texto en una matriz de recuentos de tokens"
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def buscarEnDataset(request): 
    tipo = request.data.get('analizarComentario')
    texto = request.data.get('texto')
    docs = CLOUD_DATABASE.collection(u'Comentario').stream()

    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
         
    if(tipo == 'comentario'):
        tipoData = 'lema_text'
    elif(tipo == 'resumen'): 
        tipoData = 'lema_summary'
    else:
        return Response({'status':'Error Tipo comenatario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
    print("**********:", data)
    data = procesamientoLimpieza(data)
    print(data)
    numeroComentarios, datasetTexto,rutaImg = buscarEnDatasetPalabras(data,tipoData, texto)
    return Response({ 
                    "numeroComentarios" : numeroComentarios, 
                    "comentarios": datasetTexto, 
                    "rutaImg": rutaImg
                    }, status=status.HTTP_200_OK)


def buscarEnDatasetCategorias(data, tipo):
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
    tipo = request.data.get('analizarComentario')
    categoria = request.data.get('categoria')
    clasificacionComment = request.data.get('clasificacionComment')
    
    docs = CLOUD_DATABASE.collection(u'Comentario').where(u'categoriaComentario', u'==', categoria)
    if(clasificacionComment != 'SinClasificacion'):
        docs = docs.where(u'tipo_comentario', u'==', clasificacionComment)
    docs = docs.stream()
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    if(tipo == 'comentario'):
        tipoData = 'lema_text'
    elif(tipo == 'resumen'): 
        tipoData = 'lema_summary'
    else:
        return Response({'status':'Error Tipo comenatario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    productosCollention = CLOUD_DATABASE.collection(u'Producto').stream()
    productos = pd.DataFrame()
    for doc in productosCollention:
        productos = pd.concat([productos, pd.DataFrame.from_records([doc.to_dict()])])
    
    productosComentarios = {}
    for index, row in productos.iterrows():
        nombreProducto = str(row.nombreProducto)
        docs = CLOUD_DATABASE.collection(u'Comentario').where(u'nombreProducto', u'==', nombreProducto).where(u'tipo_comentario', u'==', 'very positive').stream()
        ##Contamos cuantos comentarios con clasificacion de excelente tiene cada producto
        cantidad = len(list(docs))
        productosComentarios[nombreProducto]=cantidad
    
    productosComentarios_sort = sorted(productosComentarios.items(), key=operator.itemgetter(1), reverse=True)
    dimension = len(productosComentarios_sort) - 3
    mejoresProductos= productosComentarios_sort[:3]
    peoresProductos= productosComentarios_sort[dimension:]
    
    return Response({"mejores_productos": mejoresProductos, "peores_productos": peoresProductos}, status=status.HTTP_200_OK)
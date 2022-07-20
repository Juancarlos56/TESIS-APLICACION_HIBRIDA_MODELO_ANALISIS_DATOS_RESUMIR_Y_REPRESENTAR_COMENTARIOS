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
from nltk.corpus import stopwords

stop_words = set(stopwords.words('spanish')) 


def buscarEnDatasetPalabras(data, type, textoBuscar):
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
       return 0, 0,'not exist'

    text = " ".join(review for review in datasetTexto[type])
    wc = WordCloud(stopwords=stop_words,width=1024, height=768, background_color="white", colormap="Dark2",max_font_size=150)
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
    clasificacion = request.data.get('clasificacionComment')
    
    if(clasificacion == 'SinClasificacion'):
        docs = CLOUD_DATABASE.collection(u'Comentario').stream()
    elif(clasificacion!=''):
        docs = CLOUD_DATABASE.collection(u'Comentario').where(u'tipo_comentario', u'==', clasificacion).stream()
        
    data = pd.DataFrame()
    for doc in docs:
        data = pd.concat([data, pd.DataFrame.from_records([doc.to_dict()])])
    
    print("tipo: ",tipo)
    print("texto: ",texto)
    print("clasificacion: ",clasificacion)
         
    if(tipo == 'comentario'):
        tipoData = 'comentario_completo'
    elif(tipo == 'resumen'): 
        tipoData = 'resumen_comentario'
    else:
        return Response({'status':'Error Tipo comenatario: comentario o resumen'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = procesamientoLimpieza(data)
    numeroComentarios, datasetTexto,rutaImg = buscarEnDatasetPalabras(data,tipoData, texto)
    
    return Response({ 
                    "numeroComentarios" : numeroComentarios, 
                    "comentarios": datasetTexto, 
                    "rutaImg": rutaImg
                    }, status=status.HTTP_200_OK)



import pandas as pd 
import numpy as np
import pickle
import tensorflow as tf
import numpy as np
import pandas as pd 
from .Transformer import TextSummarizationPredict
from .PreparacionSample.preprocesamientoTexto import (TextoToDataframe, eliminarValoresNulos, limpiarNewSample)

class SummarizationPredict:
    """ Clase TextSummarizationPredict """
    
    def __init__(self) -> None:
        """ Inicia la clase TextSummarizationT5 """
        pass
   
    def cargarPipeline(self, nombreArchivo):
        """
            Funcion para cargar archivo pipeline, esta funcion no se esta utilizando pero 
            si se necesita se puede utilizar 
            Args:
                nombreArchivo (string): ruta en donde se encuentra el archivo
            return: 
                pipeline: archivo cargado
        """
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    
    def limpiezaTextoParaPredict(self, texto):  
        """
            Funcion para realizar una limpieza y transformacion a nuestro comentario
            Args:
                texto (string): comantarios que se desea analizar
            return: 
                comentario: comentarios ya limpio 
        """
        ##Conversion de texto a dataframe
        dataset = TextoToDataframe(texto)
        ##Eliminacion de valores nulos
        dataset = eliminarValoresNulos(dataset)
        ##Limpieza de caracteres del nuevo comentario
        dataset = limpiarNewSample(dataset)
        return dataset['cleaned_text'][0]
    
    def predictSummarization(self, texto):
        """
            Funcion para realizar la prediccion del comentario y obtener el resumen
            Args:
                texto (string): comantarios que se desea analizar
            return: 
                comentario: resumen obtenido 
        """
        ##creando nuestra clase del modelo transformer 
        model = TextSummarizationPredict()
        ##Path en donde se encuentra ubicado los archivos de nuestro modelo
        pathModel = "static/modelo/TextSummarizationT5/TextSummarizationT5-epoch-7-train-loss-0.4759-val-loss-1.2537"
        ##Carga de nuestro modelo transfomer t5, sin gpu
        ##************si usted tiene esta opcion ya configurada modificar a true*********
        model.load_model("t5",pathModel, use_gpu=False)
        ##Limpieza de nuestro comenatarios para correcto analisis
        text_to_summarize=self.limpiezaTextoParaPredict(texto)
        ##Obtencion de nuestro resumen
        return(model.predict(text_to_summarize)[0])
        
            
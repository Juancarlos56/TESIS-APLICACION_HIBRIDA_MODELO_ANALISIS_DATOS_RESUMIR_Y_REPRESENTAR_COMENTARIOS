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
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    
    def limpiezaTextoParaPredict(self, texto):  
        dataset = TextoToDataframe(texto)
        dataset = eliminarValoresNulos(dataset)
        dataset = limpiarNewSample(dataset)
        return dataset['cleaned_text'][0]
    
    def predictSummarization(self, texto):
        model = TextSummarizationPredict()
        pathModel = "static/modelo/TextSummarizationT5/TextSummarizationT5-epoch-7-train-loss-0.4759-val-loss-1.2537"
        model.load_model("t5",pathModel, use_gpu=False)
        text_to_summarize=self.limpiezaTextoParaPredict(texto)
        return(model.predict(text_to_summarize)[0])
        
            
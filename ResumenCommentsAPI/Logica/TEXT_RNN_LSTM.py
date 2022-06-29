#Imports
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import load_model, model_from_json
import pickle
from ResumenCommentsAPI.Logica import modelo


from tensorflow.keras.preprocessing.text import Tokenizer 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd 
#Guardar pesos y la arquitectura de la red en un archivo 
from tensorflow.keras.models import model_from_json 
from attention import AttentionLayer
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re


class TEXT_RNN_LSTM():
    
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english')) 
    ##Modelos RNN-Encoder-Decoder
    nombreArchivoModeloEncoder='modelo/arquitecturaEncoder'
    nombreArchivoPesosEncoder='modelo/pesosEncoder'
    nombreArchivoModeloDecoder='modelo/arquitecturaDecoder'
    nombreArchivoPesosDecoder='modelo/pesosDecoder'
    #Archivos de vocabulacion
    nombreArchivo_reverseTarjet='vectorizacion/reverse_target_word_index.npy'
    nombreArchivo_reverse_source='vectorizacion/reverse_source_word_index.npy'
    nombreArchivo_target_word_index='vectorizacion/target_word_index.npy'
    max_text_len=40, 
    max_summary_len=10
    
    mapeo_de_contracciones_ingles = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",
                                "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
                                "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
                                "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",
                                "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
                                "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",
                                "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",
                                "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",
                                "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
                                "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",
                                "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",
                                "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",
                                "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",
                                "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",
                                "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
                                "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",
                                "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",
                                "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
                                "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",
                                "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",
                                "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                                "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
                                "you're": "you are", "you've": "you have"}
    
    def cargarRNN(self, nombreArchivoModelo,nombreArchivoPesos):
        
        # Cargar la Arquitectura desde el archivo JSON
        with open(nombreArchivoModelo+'.json', 'r') as f:
            model = model_from_json(f.read(),custom_objects={'AttentionLayer': AttentionLayer})
        
        # Cargar Pesos (weights) en el nuevo modelo
        model.load_weights(nombreArchivoPesos+'.h5')  
        return model
    
    def cargaArchivosVocabulario(self):
        reverse_target_word_index = dict((np.load(self.nombreArchivo_reverseTarjet, allow_pickle='TRUE')).flatten()[0])
        reverse_source_word_index = dict((np.load(self.nombreArchivo_reverse_source, allow_pickle='TRUE')).flatten()[0])
        target_word_index = dict((np.load(self.nombreArchivo_target_word_index, allow_pickle='TRUE')).flatten()[0])
        return reverse_target_word_index, reverse_source_word_index, target_word_index
    
    def cargarEncoderDecoder(self):
        encoder_model= self.cargarRNN(self.nombreArchivoModeloEncoder,self.nombreArchivoPesosEncoder)
        decoder_model= self.cargarRNN(self.nombreArchivoModeloDecoder,self.nombreArchivoPesosDecoder)
        return encoder_model, decoder_model
    
    def limpiarTexto(self,texto, numero):
        newString = texto.lower() #texto en minisculas 
        newString = BeautifulSoup(newString, "html.parser").text # eliminacion de texto html
        newString = re.sub(r'\([^)]*\)', '', newString) #eliminacion de caracteres especiales
        newString = re.sub('"','', newString) #eliminacion de comillas dentro del texto
        newString = ' '.join([self.mapeo_de_contracciones_ingles[t] if t in self.mapeo_de_contracciones_ingles else t for t in newString.split(" ")]) ##Eliminacion de contracciones del texto    
        newString = re.sub(r"'s\b","",newString) ## Eliminacion de contracciones 's
        newString = re.sub("[^a-zA-Z]", " ", newString) ##Eliminacion de palabras vacias 
        newString = re.sub('[m]{2,}', 'mm', newString) 

        if(numero==0):
            tokens = [w for w in newString.split() if not w in self.stop_words]
        else:
            tokens=newString.split()
        long_words=[]
        for i in tokens:
            if len(i)>1:  #eliminacion de palabras cortas
                long_words.append(i)   
        return (" ".join(long_words)).strip()
    
    def tokenizador(self, df, max_text_len=40):
        #Preparacion de tokenizador para review de datos de train
        newSample_tokenizer = Tokenizer() 
        newSample_tokenizer.fit_on_texts(list(df['text']))
        total_words = len(newSample_tokenizer.word_index) + 1 
        newSample_tokenizer = Tokenizer(num_words=total_words) 
        newSample_tokenizer.fit_on_texts(list(df['text']))
        #convert text sequences into integer sequences
        newSample_tokenizer_seq =   newSample_tokenizer.texts_to_sequences(df['text'])
        #padding zero upto maximum length
        newSample_tokenizer =   pad_sequences(newSample_tokenizer_seq,  maxlen=max_text_len, padding='post')
        return newSample_tokenizer

    def decode_sequence(self, input_seq,encoder_model, decoder_model,target_word_index, reverse_target_word_index, max_text_len=40, max_summary_len=10):
        

        # Encode the input as state vectors.
        e_out, e_h, e_c = encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1,1))

        # Populate the first word of target sequence with the start word.
        target_seq[0, 0] = target_word_index['startinicio']

        stop_condition = False
        decoded_sentence = ''
        while not stop_condition:
            
            output_tokens, h, c = decoder_model.predict([target_seq] + [e_out, e_h, e_c])

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_token = reverse_target_word_index[sampled_token_index]


            if(sampled_token!='endfin'):
                decoded_sentence += ' '+sampled_token

            # Exit condition: either hit max length or find stop word.
            if (sampled_token == 'endfin'  or len(decoded_sentence.split()) >= (max_summary_len-1)):
                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1,1))
            target_seq[0, 0] = sampled_token_index

            # Update internal states
            e_h, e_c = h, c

        return decoded_sentence
        
        
def resumenTextoRNN_LSTM(texto="", max_text_len=40, max_summary_len=10):
    resumen = TEXT_RNN_LSTM()
    reverse_target_word_index, reverse_source_word_index, target_word_index = resumen.cargaArchivosVocabulario()
    encoder_model, decoder_model = resumen.cargarEncoderDecoder()
    text = texto
    listadoTexto = [text]
    dataset = pd.DataFrame()
    dataset['Text'] = listadoTexto
    dataset['Text'] = dataset['Text'].apply(lambda x : 'startinicio '+ x + ' endfin')
    ## Limpiamos el texto de la columna text 
    textoLimpio = []
    for t in dataset['Text']:
        textoLimpio.append(resumen.limpiarTexto(t,0))
    dataset['cleaned_text']=textoLimpio
    
    #Difinicion de tamano maximo de texto
    cleaned_text =np.array(dataset['cleaned_text'])
    short_text=[]
    for i in range(len(cleaned_text)):
        if(len(cleaned_text[i].split())<=max_text_len):
            short_text.append(cleaned_text[i])
    df=pd.DataFrame({'text':short_text})
    
    #Tokenizacion del sample
    newSample_tokenizer = resumen.tokenizador(df)
    sample_decoded_sentence = resumen.decode_sequence(newSample_tokenizer, encoder_model, decoder_model,target_word_index, reverse_target_word_index)
    return sample_decoded_sentence
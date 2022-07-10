import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from collections import Counter

def get_keys(topic_matrix):
    '''
    returns an integer list of predicted topic 
    categories for a given topic matrix
    '''
    keys = topic_matrix.argmax(axis=1).tolist()
    return keys

def keys_to_counts(keys):
    '''
    returns a tuple of topic categories and their 
    accompanying magnitudes for a given list of keys
    '''
    count_pairs = Counter(keys).items()
    categories = [pair[0] for pair in count_pairs]
    counts = [pair[1] for pair in count_pairs]
    return (categories, counts)
    


def get_top_n_words(n_topics,n, keys, document_term_matrix, tfidf_vectorizer):
    '''
    returns a list of n_topic strings, where each string contains the n most common 
    words in a predicted category, in order
    '''
    top_word_indices = []
    for topic in range(n_topics):
        temp_vector_sum = 0
        for i in range(len(keys)):
            if keys[i] == topic:
                temp_vector_sum += document_term_matrix[i]
        temp_vector_sum = temp_vector_sum.toarray()
        top_n_word_indices = np.flip(np.argsort(temp_vector_sum)[0][-n:],0)
        top_word_indices.append(top_n_word_indices)   
    top_words = []
    for topic in top_word_indices:
        topic_words = []
        for index in topic:
            temp_word_vector = np.zeros((1,document_term_matrix.shape[1]))
            temp_word_vector[:,index] = 1
            the_word = tfidf_vectorizer.inverse_transform(temp_word_vector)[0][0]
            topic_words.append(the_word)
        top_words.append(" ".join(topic_words))         
    return top_words


def topicLSA(data, tipo):

    reindexed_data = data[tipo]
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=True, )
    reindexed_data = reindexed_data.values
    document_term_matrix = tfidf_vectorizer.fit_transform(reindexed_data)
    n_topics = 4
    lsa_model = TruncatedSVD(n_components=n_topics, random_state=40)
    lsa_topic_matrix = lsa_model.fit_transform(document_term_matrix)
    lsa_keys = get_keys(lsa_topic_matrix)
    lsa_categories, lsa_counts = keys_to_counts(lsa_keys)
    top_n_words_lsa = get_top_n_words(n_topics,3, lsa_keys, document_term_matrix, tfidf_vectorizer)
    labels = ['Topic {}:'.format(i) + top_n_words_lsa[i] for i in lsa_categories]
    
    listaValores = []
    for x in range(0, len(lsa_categories)):
        listaValores.append((labels[x], lsa_categories[x], lsa_counts[x]))
    
    return listaValores
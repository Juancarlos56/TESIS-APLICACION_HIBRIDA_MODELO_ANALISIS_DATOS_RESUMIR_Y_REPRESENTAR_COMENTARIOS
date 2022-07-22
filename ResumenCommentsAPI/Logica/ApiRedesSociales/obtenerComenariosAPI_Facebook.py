import facebook as fb
import requests
import pandas as pd
import time 
from ...ClavesPrivadas.FacebookAPI import TOKEN_FACEBOOK


def obtencionComentariosPublicacionPaginaFacebook(token, idPagina_idPost):
    url = "https://graph.facebook.com/v14.0/"+str(idPagina_idPost)+"/comments?access_token="+str(token)
    output = requests.get(url).json()
    comment_data =[]
    for comment in  output['data']:
            try:
                current_comment = [comment["message"], comment["from"]["name"],  comment["from"]["id"], comment["created_time"], comment["id"]]
                comment_data.append(current_comment)
            except Exception:
                current_comment = [comment["message"], 'Facebook Profile Private', 'ID Facebook Private', comment["created_time"], comment["id"]]
                comment_data.append(current_comment)  
    return comment_data 

def obtencionUltimosPublicacionesPaginaFacebook(token, idPagina):
    url = "https://graph.facebook.com/v14.0/"+str(idPagina)+"/published_posts?access_token="+str(token)
    output = requests.get(url).json()
    postFeed =[]
    for post in  output['data']:
        try:
            postFacebook = [post["created_time"],  post["id"]]
            postFeed.append(postFacebook)
        except Exception:
            pass
    df = pd.DataFrame(postFeed, columns =['fechaCreacion', 'id_pagina_post'])
    df.head(10)
    return df


def obtencionIdPaginaFacebook(token):
    url = "https://graph.facebook.com/v14.0/me?fields=id%2Cname&access_token="+str(token)
    output = requests.get(url).json()
    return output['id']

def almacenarComentariosCSV(df):
    df.to_csv('ResumenCommentsAPI/Logica/DatasetComentarios/datasetPostFacebook.csv', sep=';', index=False)
    
def obtencionComentariosFacebook(token):
    idPage = obtencionIdPaginaFacebook(token)
    dfPublicaciones = obtencionUltimosPublicacionesPaginaFacebook(token, idPage)
    df = pd.DataFrame()
    for i in dfPublicaciones.index:
        listaComentariosPost = obtencionComentariosPublicacionPaginaFacebook(token, dfPublicaciones['id_pagina_post'][i])
        dfPost = pd.DataFrame(listaComentariosPost, columns =['comentario_completo', 'Profile Name', 'Id Facebook', 'fecha_comentario', 'id_pagina_post'])
        df = pd.concat([df, dfPost])
    df.reset_index(drop=True, inplace=True)
    almacenarComentariosCSV(df)
    return df

def main():
    df = obtencionComentariosFacebook(TOKEN_FACEBOOK)
    return df

    
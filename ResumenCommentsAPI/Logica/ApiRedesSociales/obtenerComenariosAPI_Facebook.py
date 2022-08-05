import facebook as fb
import requests
import pandas as pd
import time 
from ...ClavesPrivadas.FacebookAPI import TOKEN_FACEBOOK


def obtencionComentariosPublicacionPaginaFacebook(token, idPagina_idPost, imagen, categoriaComentario, nombreProducto):
    url = "https://graph.facebook.com/v14.0/"+str(idPagina_idPost)+"/comments?access_token="+str(token)
    output = requests.get(url).json()
    comment_data =[]
    for comment in  output['data']:
            try:
                current_comment = [idPagina_idPost, imagen, categoriaComentario, nombreProducto, comment["message"], 
                                   comment["from"]["name"],  comment["from"]["id"], 
                                   comment["created_time"], comment["id"]]
                comment_data.append(current_comment)
            except Exception:
                current_comment = [idPagina_idPost, imagen, categoriaComentario, nombreProducto, comment["message"], 
                                   'Facebook Profile Private', 'ID Facebook Private', 
                                   comment["created_time"], comment["id"]]
                comment_data.append(current_comment)  
            finally: 
                pass 
            
    return comment_data 

def obtencionUltimosPublicacionesPaginaFacebook(token, idPagina):
    url = "https://graph.facebook.com/v14.0/"+str(idPagina)+"/published_posts?fields=message%2Ccreated_time%2Cfull_picture&access_token="+str(token)
    output = requests.get(url).json()
    postFeed =[]
    for post in  output['data']:
        try:
            postFacebook = [post["created_time"],  post["id"], post["message"], post["full_picture"]]
            postFeed.append(postFacebook)
        except Exception:
            pass
    df = pd.DataFrame(postFeed, columns =['fechaCreacion', 'id_pagina_post', 'descripcion', 'imagen'])
    return df


def obtencionIdPaginaFacebook(token):
    url = "https://graph.facebook.com/v14.0/me?fields=id%2Cname&access_token="+str(token)
    output = requests.get(url).json()
    return output['id']

def almacenarComentariosCSV(df):
    df.to_csv('ResumenCommentsAPI/Logica/DatasetComentarios/datasetPostFacebook.csv', sep=';', index=False)
    
def filtrarNombreProducto(data, filtro):
    dfAux = data[data.descripcion.str.contains(str(filtro)+'?', regex=True, case=False)]
    dfAux=dfAux.assign(nombreProducto=filtro)
    return dfAux

def filtarByTipoCategoria(dfPublicaciones, filtro):
    dfAux = dfPublicaciones[dfPublicaciones.descripcion.str.contains('#'+str(filtro)+'?', regex=True, case=False)]
    dfAux=dfAux.assign(categoriaComentario=filtro)
    return dfAux

def filtrarComida(dfPublicaciones):
    listaProductoComida = ['PIZZA PREMIUM 25 CM 4 INGREDIENTES','PIZZA HAWAINA 25 CM','COSTILLAS CERDO BBQQ','PIZZA PREMIUM 31 CM 4 INGREDIENTES'
                        'PAPI CONO','PIERNITAS DE POLLO SALSA BBQQ','ALITAS BBQQ PICANTES','CHESBURGUER','PAPI POLLO BROSTER']
    dfComidaCategoriaProducto = pd.DataFrame()
    
    dfComida = filtarByTipoCategoria(dfPublicaciones, 'Comida')
    for producto in listaProductoComida:
        dfFiltrado = filtrarNombreProducto(dfComida, producto)
        if(not dfFiltrado.empty):
            dfComidaCategoriaProducto = pd.concat([dfComidaCategoriaProducto, dfFiltrado])
    return dfComidaCategoriaProducto

def serviciosRestaurante(dfPublicaciones):
    listaCategorias = ['Costo','Limpieza','Atmosfera','AtencionalCliente','Decoracion','Ubicacion']
    dfCategoria = pd.DataFrame()
    for categoria in listaCategorias:
        dfFiltrado = filtarByTipoCategoria(dfPublicaciones, categoria)
        if(not dfFiltrado.empty):
            dfFiltrado=dfFiltrado.assign(nombreProducto='General')
            dfCategoria = pd.concat([dfCategoria, dfFiltrado])
    return dfCategoria

### Eliminando comentarios de nuestra pagina por parte del admin 
def eliminarComenatariosDeAdmin(df):
    is_admin = (df.loc[:, 'Id Facebook'] != '1459951774225838')
    dfFiltrado = df.loc[is_admin]
    return dfFiltrado

def obtencionComentariosFacebook(token):
    idPage = obtencionIdPaginaFacebook(token)
    dfPublicaciones = obtencionUltimosPublicacionesPaginaFacebook(token, idPage)
    
    dfCategoriasProductos = pd.DataFrame()
    dfComida = filtrarComida(dfPublicaciones)
    dfCategoriasProductos = pd.concat([dfCategoriasProductos, dfComida])
    dfCategoria = serviciosRestaurante(dfPublicaciones)
    dfCategoriasProductos = pd.concat([dfCategoriasProductos, dfCategoria])
    df = pd.DataFrame()
    
    for i in range(len(dfCategoriasProductos)):
        listaComentariosPost = obtencionComentariosPublicacionPaginaFacebook(token, 
                                                                             dfCategoriasProductos.iloc[i]['id_pagina_post'],
                                                                             dfCategoriasProductos.iloc[i]['imagen'],
                                                                             dfCategoriasProductos.iloc[i]['categoriaComentario'],
                                                                             dfCategoriasProductos.iloc[i]['nombreProducto'])
                                                                             
        dfPost = pd.DataFrame(listaComentariosPost, columns =['idPagina_idPost','imagen', 'categoriaComentario', 'nombreProducto','comentario_completo', 'Profile Name', 'Id Facebook', 'fecha_comentario', 'id_pagina_post_comment'])
        df = pd.concat([df, dfPost])
    df.reset_index(drop=True, inplace=True)
    df = eliminarComenatariosDeAdmin(df)
    almacenarComentariosCSV(df)
    df.reset_index(drop=True, inplace=True)
    return df

def main():
    df = obtencionComentariosFacebook(TOKEN_FACEBOOK)
    return df

    
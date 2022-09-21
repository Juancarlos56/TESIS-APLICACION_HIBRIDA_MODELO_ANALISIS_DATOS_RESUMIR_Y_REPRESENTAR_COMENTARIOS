import facebook as fb
import requests
import pandas as pd
import time 
from ...ClavesPrivadas.FacebookAPI import TOKEN_FACEBOOK


def obtencionComentariosPublicacionPaginaFacebook(token, idPagina_idPost, imagen, categoriaComentario, nombreProducto):
    """
        Funciona para obtencion de los comentarios de una publicacion de facebook
        Args:
            token (string): token de facebook para acceder a la informacion
            idPagina_idPost (string): id del comentario obtenido de facebook
            categoriaComentario (string): categoria del producto publicado en facebook
            nombreProducto (string): nombre del producto publicado en facebook
            imagen (string): url de imagen del producto publicado en facebook
        return: 
            list = lista con todos los comentarios extraidos
    """
    ##Url para obtencion de comentarios de la pagina de facebook
    url = "https://graph.facebook.com/v14.0/"+str(idPagina_idPost)+"/comments?access_token="+str(token)
    output = requests.get(url).json()
    comment_data =[]
    ##Lectura de informacion obtenida y almacenamiento del id, imagen, categoria
    ##nombre, comentario, nombre de la persona, fecha
    ##Si no tiene el perfil publico se almacena como id y nombre privado 
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
    """
        Funciona para obtencion de las ultimas 25 publicacion de facebook
        Args:
            token (string): token de facebook para acceder a la informacion
            idPagina_idPost (string): id del comentario obtenido de facebook
        return: 
            dataframe = lista con todos las publicaciones extraidas
    """
    ##URL para obtener publicaciones de facebook
    url = "https://graph.facebook.com/v14.0/"+str(idPagina)+"/published_posts?fields=message%2Ccreated_time%2Cfull_picture&access_token="+str(token)
    output = requests.get(url).json()
    postFeed =[]
    ##Almacanamiento de publicaciones en dataframe
    for post in  output['data']:
        try:
            postFacebook = [post["created_time"],  post["id"], post["message"], post["full_picture"]]
            postFeed.append(postFacebook)
        except Exception:
            pass
    df = pd.DataFrame(postFeed, columns =['fechaCreacion', 'id_pagina_post', 'descripcion', 'imagen'])
    return df


def obtencionIdPaginaFacebook(token):
    """
        Funciona para obtencion del id de la pagina de facebook
        Args:
            token (string): token de facebook para acceder a la informacion
        return: 
           string: id de la pagina web
    """
    url = "https://graph.facebook.com/v14.0/me?fields=id%2Cname&access_token="+str(token)
    output = requests.get(url).json()
    return output['id']

def almacenarComentariosCSV(df):
    """
        Funciona para almacenamiento temporal de comenatarios en archivo .csv
        Args:
            df (dataframe): dataframe de comentarios recuperados
        return: 
           None
    """
    df.to_csv('ResumenCommentsAPI/Logica/DatasetComentarios/datasetPostFacebook.csv', sep=';', index=False)
    
def filtrarNombreProducto(data, filtro):
    """
        Funciona para filtrar los comentarios de facebook mediante el nombre
        Args:
            data (dataframe): dataset con todos los comentarios de facebook
            filtro (string): palabra por la cual se va a filtrar los comentarios
        return: 
            dataframe = dataset filtrado 
    """
    ##Utilizando regex de pandas para almacenar todos los comentarios 
    ##en donde se menciona la palabra que contiene filtro 
    ##la busqueda solo se hace dentro de la columna descripcion
    dfAux = data[data.descripcion.str.contains(str(filtro)+'?', regex=True, case=False)]
    dfAux=dfAux.assign(nombreProducto=filtro)
    return dfAux

def filtarByTipoCategoria(dfPublicaciones, filtro):
    """
        Funciona para filtrar los comentarios segun el tipo de categoria  
        Args:
            dfPublicaciones (dataframe): dataset con todos los comentarios de facebook
            filtro (string): palabra por la cual se va a filtrar los comentarios
        return: 
            dataframe = dataset filtrado 
    """
    ##Siempre cuando se separa por categoria se debe tener el caracter de tipo # en donde 
    ##se indica a que tipo de categoria pertenece al plato
    ##*************Optimizar esto para que se mas facil **************
    dfAux = dfPublicaciones[dfPublicaciones.descripcion.str.contains('#'+str(filtro)+'?', regex=True, case=False)]
    dfAux=dfAux.assign(categoriaComentario=filtro)
    return dfAux

def filtrarComida(dfPublicaciones):
    """
        Funciona para filtrar los comentarios segun el plato de comida escogido
        Args:
            dfPublicaciones (dataframe): dataset con todos los comentarios de facebook
            filtro (string): palabra por la cual se va a filtrar los comentarios
        return: 
            dataframe = dataset filtrado por categoria y producto
    """
    ##Lista de platos de comida de nuestro restaurante 
    ##los mismo existentes de la base de datos
    ##*******Optimizar este proceso para no tener que estar agregando cada nuevo***********
    ##plato dentro de esta lista. 
    listaProductoComida = ['PIZZA PREMIUM 25 CM 4 INGREDIENTES','PIZZA HAWAINA 25 CM','COSTILLAS CERDO BBQQ','PIZZA PREMIUM 31 CM 4 INGREDIENTES'
                        'PAPI CONO','PIERNITAS DE POLLO SALSA BBQQ','ALITAS BBQQ PICANTES','CHESBURGUER','PAPI POLLO BROSTER']
    dfComidaCategoriaProducto = pd.DataFrame()
    ##Filtramos primero por comida para solo tener comenatios recpecto a esta. 
    dfComida = filtarByTipoCategoria(dfPublicaciones, 'Comida')
    
    for producto in listaProductoComida:
        ##Filtramos por cada uno de nuestros platos y si es que se 
        ##tiene algun resultado agregamos este resultado a nuestro dataframe
        dfFiltrado = filtrarNombreProducto(dfComida, producto)
        if(not dfFiltrado.empty):
            dfComidaCategoriaProducto = pd.concat([dfComidaCategoriaProducto, dfFiltrado])
    return dfComidaCategoriaProducto

def serviciosRestaurante(dfPublicaciones):
    """
        Funciona para analizar los comenatarios de nuestro restaurante con respecto 
        a distintos tipos de servicios
        Args:
            dfPublicaciones (dataframe): dataset con todos los comentarios de facebook
        return: 
            dataframe = dataset filtrado por servicio
    """
    ##Lista de servicios que se manejan dentro del restaurante 
    ##los mismo de la base de datos 
    ##***********optimizar esto para no tener que agregar cada vez un nuevo servicio************
    listaCategorias = ['Costo','Limpieza','Atmosfera','AtencionalCliente','Decoracion','Ubicacion']
    dfCategoria = pd.DataFrame()
    for categoria in listaCategorias:
        ##LLamada al metodo que permite filtrar por categorias
        dfFiltrado = filtarByTipoCategoria(dfPublicaciones, categoria)
        if(not dfFiltrado.empty):
            dfFiltrado=dfFiltrado.assign(nombreProducto='General')
            dfCategoria = pd.concat([dfCategoria, dfFiltrado])
    return dfCategoria
 
def eliminarComenatariosDeAdmin(df):
    """
        Eliminando comentarios de nuestra pagina por parte del admin
        Args:
            df (dataframe): dataset con todos los comentarios de facebook
        return: 
            dataframe = dataset sin comentarios de admin
    """
    is_admin = (df.loc[:, 'Id Facebook'] != '1459951774225838')
    dfFiltrado = df.loc[is_admin]
    return dfFiltrado

def obtencionComentariosFacebook(token):
    """
        obtencion de comentarios de nuestra pagina de facebook
        Args:
            token (string): token de la pagina de facebook
        return: 
            dataframe = dataset listo para uso de frontend
    """
    ##Obtencion de id de la pagina 
    idPage = obtencionIdPaginaFacebook(token)
    ##Obtencion de las 25 primeras publicaciones de facebook
    dfPublicaciones = obtencionUltimosPublicacionesPaginaFacebook(token, idPage)
    
    dfCategoriasProductos = pd.DataFrame()
    ##Filtrando comentarios por tipo de comida
    dfComida = filtrarComida(dfPublicaciones)
    dfCategoriasProductos = pd.concat([dfCategoriasProductos, dfComida])
    ##Filtrando comentarios por tipo de servicio de restaurante
    dfCategoria = serviciosRestaurante(dfPublicaciones)
    ##Dataset con tipo de servicio y comida
    dfCategoriasProductos = pd.concat([dfCategoriasProductos, dfCategoria])

    df = pd.DataFrame()
    for i in range(len(dfCategoriasProductos)):
        listaComentariosPost = obtencionComentariosPublicacionPaginaFacebook(token, 
                                                                             dfCategoriasProductos.iloc[i]['id_pagina_post'],
                                                                             dfCategoriasProductos.iloc[i]['imagen'],
                                                                             dfCategoriasProductos.iloc[i]['categoriaComentario'],
                                                                             dfCategoriasProductos.iloc[i]['nombreProducto'])
        ##Comentarios de post facebook                                                                
        dfPost = pd.DataFrame(listaComentariosPost, columns =['idPagina_idPost','imagen', 'categoriaComentario', 'nombreProducto','comentario_completo', 'Profile Name', 'Id Facebook', 'fecha_comentario', 'id_pagina_post_comment'])
        ##Almacenamiento de comenario con repecto a servicio y comida
        df = pd.concat([df, dfPost])
    df.reset_index(drop=True, inplace=True)
    df = eliminarComenatariosDeAdmin(df)
    almacenarComentariosCSV(df)
    df.reset_index(drop=True, inplace=True)
    return df

def main():
    df = obtencionComentariosFacebook(TOKEN_FACEBOOK)
    return df
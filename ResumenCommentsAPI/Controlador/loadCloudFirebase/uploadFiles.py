from ResumenCommentsAPI.ClavesPrivadas.FirebaseConfig import STORAGE


def subirArchivosStorage(fileNamelocal,fileNameCloud):
    """
        Funcion para almacenar archivos dentro de storage de firebase
        Args:
            fileNamelocal(string): ubicacion local del documento 
            fileNameCloud(string): ubicacion en la nube del documento
        return: 
            url(string): retorna la URL en donde se encuentra ubicado nuestro archivo
    """
    # Put your local file path 
    STORAGE.child(fileNameCloud).put(fileNamelocal)
    return STORAGE.child(fileNameCloud).get_url(None)

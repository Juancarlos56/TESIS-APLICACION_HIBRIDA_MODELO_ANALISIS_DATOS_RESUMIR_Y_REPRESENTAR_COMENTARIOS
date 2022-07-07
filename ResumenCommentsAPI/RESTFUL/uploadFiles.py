from ResumenCommentsAPI.ClavesPrivadas.FirebaseConfig import STORAGE


def subirArchivosStorage(fileNamelocal,fileNameCloud):
    # Put your local file path 
    STORAGE.child(fileNameCloud).put(fileNamelocal)
    return STORAGE.child(fileNameCloud).get_url(None)

from django.shortcuts import render
import pyrebase

#code Firebase, credenciales del proyecto.
config={
    "apiKey": "AIzaSyB5Kv8v_DpH6GeMEeHcmExz4o0P-8OFjoU",
    "authDomain": "aplicacion-resumen-comentarios.firebaseapp.com",
    "projectId": "aplicacion-resumen-comentarios",
    "storageBucket": "aplicacion-resumen-comentarios.appspot.com",
    "messagingSenderId": "973370360772",
    "appId": "1:973370360772:web:f972e443a570ff352f9a91"
}

#here we are doing firebase authentication
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
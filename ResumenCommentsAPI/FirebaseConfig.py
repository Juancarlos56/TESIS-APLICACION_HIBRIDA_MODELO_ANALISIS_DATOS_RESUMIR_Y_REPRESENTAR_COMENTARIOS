from django.shortcuts import render
import pyrebase
import environ
from pathlib import Path
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'enviroment.env'))


#code Firebase, credenciales del proyecto.
#esta configuracion nos sirve para manipular realtime database
config={
    "apiKey": env('apiKey'),
    "authDomain": "aplicacion-resumen-comentarios.firebaseapp.com",
    "projectId": "aplicacion-resumen-comentarios",
    "storageBucket": "aplicacion-resumen-comentarios.appspot.com",
    "messagingSenderId": env('messagingSenderId'),
    "appId":  env('appId'),
    "databaseURL":""
}

#here we are doing firebase authentication
firebase=pyrebase.initialize_app(config)
AUTHE = firebase.auth()
REAL_DATABASE = firebase.database()
STORAGE = firebase.storage()



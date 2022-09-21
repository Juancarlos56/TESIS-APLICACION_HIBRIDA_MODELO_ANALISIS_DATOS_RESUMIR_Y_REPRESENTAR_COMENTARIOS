from django.shortcuts import render
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
##Ubucacion de credenciales de facebook
environ.Env.read_env(os.path.join(BASE_DIR, 'vars/enviroment.env'))
##Nombre de credencial de facebook
TOKEN_FACEBOOK = env('tokenAPI')
##Nombre de credencial de api para clasificacion de comentarios
TOKEN_RAPID_API = env('tokenApiClasificacion')
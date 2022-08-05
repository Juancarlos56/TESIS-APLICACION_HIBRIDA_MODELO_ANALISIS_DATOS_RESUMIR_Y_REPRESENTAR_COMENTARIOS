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
environ.Env.read_env(os.path.join(BASE_DIR, 'vars/enviroment.env'))

TOKEN_FACEBOOK = env('tokenAPI')

TOKEN_RAPID_API = env('tokenApiClasificacion')
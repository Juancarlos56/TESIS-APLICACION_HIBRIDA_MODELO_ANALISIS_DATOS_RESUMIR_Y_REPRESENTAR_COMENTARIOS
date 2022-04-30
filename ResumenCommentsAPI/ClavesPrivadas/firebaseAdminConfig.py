import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

##Carga del archivo de configuracion para manipulacion de firebase
cred = credentials.Certificate("ResumenCommentsAPI\ClavesPrivadas\serviceAccount.json")
firebase_admin.initialize_app(cred)

##Creacion de variable para manipular Firestore database 
CLOUD_DATABASE = firestore.client()
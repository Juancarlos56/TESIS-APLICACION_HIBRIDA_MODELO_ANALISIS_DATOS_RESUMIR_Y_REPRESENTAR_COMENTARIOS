import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("ResumenCommentsAPI\ClavesPrivadas\serviceAccount.json")
firebase_admin.initialize_app(cred)
CLOUD_DATABASE = firestore.client()
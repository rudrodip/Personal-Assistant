import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('TextProcessing/cred.json')
firebase_admin.initialize_app(cred)

print('successfully initialized firebase')

db = firestore.client()
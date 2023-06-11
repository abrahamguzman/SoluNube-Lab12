from firebase_admin import credentials, firestore, db
import firebase_admin

# Configurar las credenciales de Firebase
cred = credentials.Certificate('database.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://lab08-crud-default-rtdb.firebaseio.com/'
})
ref = db.reference('items')

def addMovie(datos):
    ref.push(datos)
    
def editMovie(id, datos):
    ref.child(id).update(datos)

def deleteMovie(id):
    ref.child(id).delete()
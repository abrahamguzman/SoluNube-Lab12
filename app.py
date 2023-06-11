from flask import Flask, redirect, url_for, render_template, jsonify, request
from functionsS3 import cargarS3, eliminarS3, bucket_name, editarS3
from functionsDB import addMovie, editMovie, deleteMovie, ref
import os

# Creamos instancia de Flask
app = Flask(__name__)

@app.route('/')
def index():
    datos = ref.get()
    bucket = bucket_name
    return render_template('index.html', datos=datos, bucket = bucket)
    
@app.route('/crear')
def crear():
    return render_template('crear.html')

@app.route('/creado', methods=['POST'])
def creado(): 
    file = request.files['image']
    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)
    
    datos = {
        'codigo': request.form['codigo'],
        'nombre': request.form['nombre'],
        'correo': request.form['correo'],
        'edad': request.form['edad'],
        'img': file.filename
    } 
    
    addMovie(datos)
    cargarS3(file.filename, filepath)
    os.remove(filepath)
    
    return redirect(url_for('index'))

@app.route('/editar/<id>/<img>')
def editar(id, img):
    datos = {
        'file_name': img,
        'id': id,
        'codigo': ref.child(id).child('codigo').get(),
        'nombre': ref.child(id).child('nombre').get(),
        'correo': ref.child(id).child('correo').get(),
        'edad': ref.child(id).child('edad').get(),
    }
    return render_template('editar.html', datos = datos)

@app.route('/editado/<id>/<img>/', methods=['POST'])
def editado(id, img):
    file = request.files['image']
    datos = {
        'codigo': request.form['codigo'],
        'nombre': request.form['nombre'],
        'correo': request.form['correo'],
        'edad': request.form['edad'],
    }
    
    if file.filename != '':
        filepath = os.path.join('static/uploads', file.filename)
        file.save(filepath)
        cargarS3(file.name, filepath)
        eliminarS3(img)
        datos['img'] = file.filename
        
        os.remove(filepath) 
        
    editMovie(id, datos)
    return redirect(url_for('index'))

@app.route('/eliminado/<id>/<img>')
def eliminado(id, img):
    deleteMovie(id)
    #eliminarS3(img)
    return redirect('/')

    
# Errores
def paginaNoEncontrada(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    app.register_error_handler(404, paginaNoEncontrada)
    app.run(debug = True, port = 5000)

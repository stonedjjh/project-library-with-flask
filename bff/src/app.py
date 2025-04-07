"""
Este módulo define una aplicación web Flask que actúa como BFF (Backend For Frontend)
para gestionar una biblioteca de libros mediante un microservicio.

Funcionalidades:
- Listar libros.
- Prestar libros.
- Devolver libros.
- Guardar libros.
- Buscar libros por ISBN.

"""

import sys
import requests

try:
    from flask import Flask, request, jsonify, render_template
except ImportError:
    print(
        "Error: Flask no está instalado. Por favor, instálalo con 'pip install Flask'"
    )
    sys.exit(1)

app = Flask(__name__)

# URL base del microservicio de libros
# URL_BASE_BOOK_SERVICE = "http://127.0.0.1:5001/api/v1/libros"
# local
# URL_BASE_BOOK_SERVICE = "http://book-service:5001/api/v1/libros"
# servidor
URL_BASE_BOOK_SERVICE = "https://book-service-99lq.onrender.com/api/v1/libros"


@app.route("/")
def index():
    """
    Esta función maneja la ruta raíz ('/') de la aplicación.
    Renderiza la plantilla 'index.html' que sirve como página principal.
    """
    # Realizar la petición al microservicio para listar los libros
    response = requests.get(URL_BASE_BOOK_SERVICE, timeout=10)
    # Comprobar si la petición ha sido exitosa
    if response.status_code == 200:
        # Convertir la respuesta a JSON
        libros = response.json()
    else:
        libros = []  # O manejar el error de alguna otra forma

    # Renderizar la plantilla index.html con los libros como contexto
    return render_template("index.html", libros=libros)


def listar_libros_microservicio():
    """
    (str)->str
    Esta función maneja la ruta "/listar" de la aplicación.
    Hace una petición al microservicio de libros para obtener la lista de libros.
    Devuelve un json con la lista de los libros.
    """

    response = requests.get(URL_BASE_BOOK_SERVICE, timeout=10)
    return response.json()


def prestar_libro_microservicio(libro_id):
    """
    (str)->json
    Esta función maneja la ruta "/prestar/<int:id>" de la aplicación.
    Hace una petición al microservicio de libros para prestar el libro.
    Devuelve un mensaje JSON indicando si el libro fue prestado o no.
    """
    url = f"{URL_BASE_BOOK_SERVICE}/{libro_id}/prestar"
    response = requests.put(url, timeout=10)
    return response.json()


def devolver_libro_microservicio(libro_id):
    """
    (str)->json
    Esta función maneja la ruta "/devolver/<int:id>" de la aplicación.
    Hace una petición al microservicio de libros para devolver el libro.
    Devuelve un mensaje JSON indicando si el libro fue devuelto o no.
    """
    url = f"{URL_BASE_BOOK_SERVICE}/{libro_id}/devolver"
    response = requests.put(url, timeout=10)
    return response.json()


def guardar_libro_microservicio():
    """
    Esta función maneja la ruta "/guardar" de la aplicación.
    Hace una petición al microservicio de libros para guardar un libro.
    Recibe los datos del libro a través de un formulario POST.
    Devuelve un mensaje JSON indicando si el libro fue guardado o no.
    """

    titulo = request.form.get("titulo")
    isbn = request.form.get("isbn")
    autor = request.form.get("autor")
    disponible = request.form.get("disponible") == "true"
    if not all([titulo, isbn, autor, disponible is not None]):
        return jsonify({"message": "Faltan datos", "success": False})

    data = {
        "titulo": titulo,
        "isbn": isbn,
        "autor": autor,
        "disponible": disponible,
    }
    response = requests.post(URL_BASE_BOOK_SERVICE, data=data, timeout=10)
    return response.json()


def buscar_libro_por_isbn(isbn):
    """
    (str)->json
    Esta función maneja la ruta "/buscar/<string:isbn>" de la aplicación.
    Hace una petición al microservicio de libros para buscar el libro.
    Devuelve un json con la información del libro o un mensaje de error.
    """
    url = f"{URL_BASE_BOOK_SERVICE}/{isbn}"
    response = requests.get(url, timeout=10)
    return response.json()


@app.route("/listar")
def listar():
    """
    Esta función maneja la ruta "/listar" de la aplicación.
    Hace una petición al microservicio de libros para obtener la lista de libros.
    Devuelve un json con la lista de los libros.
    """
    return listar_libros_microservicio()


@app.route("/prestar/<int:libro_id>", methods=["PUT"])
def prestar(libro_id):
    """
    (str)->json
    Esta función maneja la ruta "/prestar/<int:id>" de la aplicación.
    Hace una petición al microservicio de libros para prestar el libro.
    Devuelve un mensaje JSON indicando si el libro fue prestado o no.
    """
    return prestar_libro_microservicio(libro_id)


@app.route("/devolver/<int:libro_id>", methods=["PUT"])
def devolver(libro_id):
    """
    (str)->json
    Esta función maneja la ruta "/devolver/<int:id>" de la aplicación.
    Hace una petición al microservicio de libros para devolver el libro.
    Devuelve un mensaje JSON indicando si el libro fue devuelto o no.
    """
    return devolver_libro_microservicio(libro_id)


@app.route("/guardar", methods=["POST"])
def guardar():
    """
    Esta función maneja la ruta "/guardar" de la aplicación.
    Hace una petición al microservicio de libros para guardar un libro.
    Recibe los datos del libro a través de un formulario POST.
    Devuelve un mensaje JSON indicando si el libro fue guardado o no.
    """
    return guardar_libro_microservicio()


@app.route("/buscar/<string:libro_isbn>")
def buscar(libro_isbn):
    """
    (str)->json
    Esta función maneja la ruta "/buscar/<string:isbn>" de la aplicación.
    Hace una petición al microservicio de libros para buscar el libro.
    Devuelve un json con la información del libro o un mensaje de error.
    """
    return buscar_libro_por_isbn(libro_isbn)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

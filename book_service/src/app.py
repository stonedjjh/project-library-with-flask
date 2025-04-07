"""
Este módulo define una aplicación web Flask para gestionar una biblioteca de libros.

Funcionalidades:
- Listar libros.
- Prestar libros.
- Devolver libros.
- Guardar libros.

"""

import sys

try:
    from flask import Flask, request, jsonify
except ImportError:
    print(
        "Error: Flask no está instalado. Por favor, instálalo con 'pip install Flask'"
    )
    sys.exit(1)

import clase_libro

app = Flask(__name__)
mi_biblioteca = clase_libro.Biblioteca()  # Se crea la instancia de biblioteca

libros_inicio = [
    ["Cien años de soledad", "Gabriel García Márquez", "978-0307474727", True],
    ["1984", "George Orwell", "978-0451524935", True],
    ["Orgullo y prejuicio", "Jane Austen", "978-0141439518", True],
    ["El señor de los anillos", "J.R.R. Tolkien", "978-0618260231", True],
    ["Matar un ruiseñor", "Harper Lee", "978-0061120084", True],
    ["Don Quijote de la Mancha", "Miguel de Cervantes", "978-8420471899", True],
    ["El guardián entre el centeno", "J.D. Salinger", "978-0316769174", True],
    ["Crimen y castigo", "Fyodor Dostoevsky", "978-0679734505", True],
    ["En busca del tiempo perdido", "Marcel Proust", "978-0141180331", True],
    ["Ulises", "James Joyce", "978-0679722762", True],
]
for libro in libros_inicio:
    mi_biblioteca.agregar_clase_libro(
        clase_libro.Libro(libro[0], libro[1], libro[2], libro[3])
    )


@app.route("/api/v1/libros")
def listar_libros():
    """
    Esta función maneja la ruta "/api/v1/libros" de la aplicación.
    Devuelve una lista de todos los libros en la biblioteca en formato JSON.
    """

    return mi_biblioteca.mostrar_libros()


@app.route("/api/v1/libros/<int:libro_id>/prestar", methods=["PUT"])
def prestar_libro(libro_id):
    """
    (int)->json
    Esta función maneja la ruta "/api/v1/libros/<int:id>/prestar" de la aplicación.
    Permite prestar un libro de la biblioteca mediante su ID.
    Devuelve un mensaje JSON indicando si el libro fue prestado o no.
    """

    result = mi_biblioteca.prestar_libro(libro_id)
    if result:
        return jsonify({"message": "Libro prestado", "success": True})
    if result is None:
        return jsonify({"message": "ID de libro incorrecto.", "success": False})
    return jsonify({"message": "El libro no está disponible", "success": False})


@app.route("/api/v1/libros/<int:libro_id>/devolver", methods=["PUT"])
def devolver_libro(libro_id):
    """
    (int)->json
    Esta función maneja la ruta "/api/v1/libros/<int:id>/devolver" de la aplicación.
    Permite devolver un libro a la biblioteca mediante su ID.
    Devuelve un mensaje JSON indicando si el libro fue devuelto o no.
    """

    result = mi_biblioteca.devolver_libro(libro_id)
    if result:
        return jsonify({"message": "Libro devuelto", "success": True})
    if result is None:
        return jsonify({"message": "ID de libro incorrecto.", "success": False})
    return jsonify({"message": "El libro no está disponible", "success": False})


@app.route("/api/v1/libros", methods=["POST"])
def guardar_libro():
    """
    Esta función maneja la ruta "/api/v1/libros" de la aplicación.
    Permite guardar un libro en la biblioteca.
    Recibe los datos del libro a través de un formulario POST.
    Devuelve un mensaje JSON indicando si el libro fue guardado o no.
    """

    titulo = request.form.get("titulo")
    isbn = request.form.get("isbn")
    autor = request.form.get("autor")
    disponible = request.form.get("disponible") == "true"

    if not all([titulo, isbn, autor, disponible is not None]):
        return jsonify({"message": "Faltan datos", "success": False})

    try:
        mi_biblioteca.agregar_clase_libro(
            clase_libro.Libro(titulo, autor, isbn, disponible)
        )
        return jsonify({"message": "Libro guardado", "success": True})
    except ValueError as e:
        return jsonify(
            {"message": f"Error en los datos del libro: {e}", "success": False}
        )
    except TypeError as e:
        return jsonify({"message": f"Error en el tipo de dato: {e}", "success": False})


@app.route("/api/v1/libros/<string:isbn>")
def buscar_libro_por_isbn(isbn):
    """
    (str)->json
    Esta función maneja la ruta "/api/v1/libros/<string:isbn>" de la aplicación.
    Permite buscar un libro en la biblioteca mediante su ISBN.
    Devuelve un mensaje JSON con la información del libro o un mensaje de error.
    """
    result = mi_biblioteca.buscar_libro_exacto(isbn)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

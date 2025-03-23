"""
Este módulo define la clase Libro y proporciona funcionalidades para gestionar libros.

Funcionalidades:
- Creación de objetos Libro.
- Almacenamiento y recuperación de información de libros.
- ... (otras funcionalidades)
"""
import json

# se define la clase libro
class Libro:
    """
    Esta clase representa un libro en la biblioteca.

    Atributos:
        titulo (str): El título del libro.
        autor (str): El autor del libro.
        isbn (str): El ISBN del libro.
        disponible (bool): Indica si el libro está disponible para préstamo.
        id (int): El id del libro.
    """
    ID_COUNTER = 0  # Atributo estático para el contador de IDs

    def __init__(self, titulo: str, autor: str, isbn: str, disponible: bool):
        """
        (Libro, str, str, bool) -> None
        Inicializa un libro con su título, autor, idbn y disponibilidad.
        """
        Libro.ID_COUNTER += 1  # Se incrementa el contador de la clase
        self.id = Libro.ID_COUNTER  # Se asigna el ID al libro
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible

    def cambiar_disponibilidad(self):
        """
        (Libro) -> None
        Cambia la disponibilidad del libro.
        >>>true ->false
        >>>false ->true
        """
        self.disponible = not self.disponible

    def get_disponibilidad(self):
        """
        (Libro) -> bool
        Devuelve la disponibilidad del libro.
        >>>true
        >>>false
        """
        return self.disponible

    def get_isbn(self):
        """
        (Libro) -> str
        Devuelve el isbn del libro.
        """
        return self.isbn

# definimos la clase biblioteca que tiene una lista de libros
class Biblioteca:
    """
    Esta clase representa una biblioteca que contiene una lista de libros.

    Atributos:
        libros (list): Una lista de objetos Libro.
    """

    def __init__(self):
        """
        (biblioteca) -> None
        Inicializa una biblioteca con una lista vacia de libros.
        """
        self.libros = []

    def agregar_clase_libro(self, libro: Libro):
        """
        (biblioteca, libro) -> None
        Agrega un libro a la biblioteca.
        """
        self.libros.append(libro)

    def prestar_libro(self, libro_id: int):
        """
        (biblioteca, int) -> bool or None
        Presta un libro de la biblioteca mediante su ID.
        """
        try:
            libro= self.buscar_libro_por_id(libro_id)
            if libro.get_disponibilidad():
                libro.cambiar_disponibilidad()
                return True
            return False
        except IndexError:
            print("Error: Índice fuera de rango al prestar el libro.")
            return None

    def devolver_libro(self, libro_id: int):
        """
        (biblioteca, int) -> bool or None
        Devuelve un libro a la biblioteca.
        """
        try:
            libro= self.buscar_libro_por_id(libro_id)
            if not libro.get_disponibilidad():
                libro.cambiar_disponibilidad()
                return True
            return False
        except IndexError:
            print("Error: Índice fuera de rango al devolver el libro.")
            return None

    def mostrar_libros(self):
        """
        (biblioteca) -> str
        Muestra los libros de la biblioteca.
        """
        if len(self.libros) > 0:
            libros_data = []
            for libro in self.libros:
                libros_data.append(
                    {
                        "id": libro.id,
                        "titulo": libro.titulo,
                        "autor": libro.autor,
                        "isbn": libro.isbn,
                        "disponible": libro.disponible,
                    }
                )
            # Devolver los datos como un json
            return json.dumps(libros_data, indent=4)
        # Devolver un json con el mensaje de error.
        return json.dumps({"message": "No hay libros en la biblioteca."})

    def buscar_libro_por_id(self, libro_id: int):
        """
        (biblioteca, int) -> Libro or None
        Busca un libro por su ID, coincidiendo exactamente con el ID pasado como parámetro.
        """
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None

    def buscar_libro_exacto(self, isbn: str):
        """
        (biblioteca, str) -> Libro or None
        Busca un libro por su isbn, coincidiendo exactamente con el isbn pasado como parámetro.
        """
        for libro in self.libros:
            if libro.isbn == isbn:
                return json.dumps(
                    {
                        "id":libro.id,
                        "titulo": libro.titulo,
                        "autor": libro.autor,
                        "isbn": libro.isbn,
                        "disponible": libro.disponible,   
                        "success":True
                    },
                    indent=4
                )
        return json.dumps({"message": "No se encontró el libro."}, indent=4)

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
    """

    def __init__(self, titulo: str, autor: str, isbn: str, disponible: bool):
        """
        (Libro, str, str, bool) -> None
        Inicializa un libro con su título, autor, idbn y disponibilidad.
        """
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

    def get_info(self):
        """
        (Libro) -> str
        Devuelve la información del libro.
        """
        return (
            f"El libro {self.titulo} de {self.autor} con isbn {self.isbn} "
            f"{'está disponible' if self.disponible else 'no está disponible'}."
        )


    def mostrar_info(self):
        """
        (Libro) -> str
        Devuelve la información del libro.
        """
        print(
            f"El libro {self.titulo} de {self.autor} con isbn {self.isbn} "
            f"{'está disponible' if self.disponible else 'no está disponible'}."
        )


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

    def agregar_libro(self):
        """
        (biblioteca) -> None
        Agrega un libro a la biblioteca.
        """
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        isbn = input("Ingrese el isbn del libro: ")
        disponible = input("El libro está disponible? (s/n): ")
        disponible = disponible == "s"
        try:
            self.libros.append(Libro(titulo, autor, isbn, disponible))
        except ValueError as e:
            print(f"Error en los datos del libro: {e}")
        except TypeError as e:
            print(f"Error en el tipo de dato: {e}")

    def prestar_libro(self, libro_id: int):
        """
        (biblioteca, int) -> bool or None
        Presta un libro de la biblioteca mediante su ID.
        """
        try:
            if 0 <= libro_id < len(self.libros):
                libro= self.libros[libro_id]
                if libro.get_disponibilidad():
                    libro.cambiar_disponibilidad()
                    return True
                return False
            return None
        except IndexError:
            print("Error: Índice fuera de rango al prestar el libro.")
            return None

    def devolver_libro(self, libro_id: int):
        """
        (biblioteca, int) -> bool or None
        Devuelve un libro a la biblioteca.
        """
        try:
            if 0 <= libro_id < len(self.libros):
                libro = self.libros[libro_id]
                if not libro.get_disponibilidad():
                    libro.cambiar_disponibilidad()
                    return True
                return False
            return None
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
            for index, libro in enumerate(self.libros):
                libros_data.append(
                    {
                        "id": index,
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

    def buscar_libro(self, isbn: str):
        """
        (biblioteca, str) -> list
        Busca un libro por su isbn.
        """
        return list(filter(lambda self: isbn in self.isbn, self.libros))

    def buscar_libro_exacto(self, isbn: str):
        """
        (biblioteca, str) -> Libro or None
        Busca un libro por su isbn, coincidiendo exactamente con el isbn pasado como parámetro.
        """
        for libro in self.libros:
            if libro.isbn == isbn:
                return json.dumps(
                    {
                        "titulo": libro.titulo,
                        "autor": libro.autor,
                        "isbn": libro.isbn,
                        "disponible": libro.disponible,   
                        "success":True
                    },
                    indent=4
                )
        return json.dumps({"message": "No se encontró el libro."}, indent=4)

# Sistema de Gestión de Biblioteca

**Versión:** 1.0

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Sistema de Gestión de Biblioteca**, el cual permitirá llevar un inventario de libros, gestionar préstamos y devoluciones.  Esta herramienta web estará diseñada para ser utilizada por el personal de la biblioteca, quienes podrán:

*   Registrar libros.
*   Registrar usuarios de la biblioteca.
*   Gestionar préstamos de libros a usuarios.
*   Gestionar devoluciones de libros.
*   Ver registros de préstamos por usuario y por libro.

## Objetivos

El objetivo principal de este proyecto es crear una aplicación web completa que facilite la gestión de una biblioteca. En su versión inicial, se busca cumplir con los siguientes objetivos:

*   Implementar un sistema que permita registrar libros y gestionar su disponibilidad.
*  Realizar el login para los usuarios de la app.
*   Dividir el proyecto en microservicios.
*   Aplicar metodologías ágiles en el desarrollo.
*   Aprovechar los principios de CI/CD (Integración Continua/Entrega Continua).

## Funcionalidades Iniciales (Versión 1.0)

*   **Gestión de Libros:**
    *   Agregar un nuevo libro (título, autor, ISBN, disponibilidad).
    *   Prestar un libro (buscar por ISBN).
    *   Devolver un libro (buscar por ISBN).
    *   Mostrar todos los libros y su estado (disponible o no).
    *   Buscar un libro por su ISBN.

## Tecnologías

*   **Backend:**
    *   **Lenguaje:** Python
    *   **Framework:** Flask
*   **Frontend:**
    *   *Por definir*
*   **Base de Datos:**
    *   *Por definir*
* **Microservicios:**
    * *Por definir*
* **CI/CD:**
    * *Por definir*

## Estructura del Equipo

*   **Desarrollo:**
    *   **Frontend:** Responsable del diseño y la implementación de la interfaz de usuario.
    *   **Backend:** Responsable de la lógica del negocio, las APIs y la gestión de datos.
*   **Base de Datos:** Responsable del diseño y la gestión de la base de datos.
*   **QA:** Responsable de las pruebas y la calidad del software.

## Requisitos Iniciales (Basados en el Enunciado)

El proyecto se inspira en los siguientes requisitos iniciales solicitados en el curso:

1.  **Clase Libro:**
    *   Atributos: `titulo` (str), `autor` (str), `isbn` (str), `disponible` (bool, inicialmente `True`).
    *   Métodos:
        *   `agregar()`: Permite introducir un nuevo libro.
        *   `prestar()`: Cambia el estado de `disponible` a `False`.
        *   `devolver()`: Cambia el estado de `disponible` a `True`.
        *   `mostrar()`: Muestra una lista con todos los libros.
        *   `buscar()`: Busca un libro por su ISBN.
2.  **Gestión del inventario:**
    *   Uso de una lista para almacenar objetos de la clase `Libro`.
    *   Bucle para interactuar con el usuario mediante un menú:
        *   a) Agregar un nuevo libro.
        *   b) Prestar un libro.
        *   c) Devolver un libro.
        *   d) Mostrar todos los libros.
        *   e) Salir.
3.  **Condiciones:**
    *   Validar que el ISBN exista antes de prestar o devolver.
    *   Mensaje de error para opciones inválidas en el menú.


## Próximos Pasos

*   Definir las tecnologias faltantes, como frontend, bases de datos, microservicios, CI/CD.
*   Diseñar la estructura de los microservicios.
*   Planificar el sistema de login.
*   Refactorizar el código actual para adaptarlo a los microservicios.
* **Mover la logica de negocio al backend.**
* **Realizar pruebas unitarias.**
* **Realizar pruebas de integracion.**

## Etapas

1.  **Etapa 1 (Versión 1.0):**
    *   Definir las tecnologias a usar.
    *   Implementar el **sistema de login** para los usuarios.
    *   Dividir el proyecto en **microservicios**.


## Autor

Daniel Jiménez

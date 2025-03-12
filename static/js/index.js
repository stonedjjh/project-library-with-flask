class TablaLibros extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.data = [];
    this.currentPage = 1;
    this.filteredData = [];
    this.itemsPerPage = 5; // Cantidad de items por página
    this.searchTerm = ""; // Almacenar el término de búsqueda
  }

  static get observedAttributes() {
    return ["data"];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === "data") {
      try {
        this.data = JSON.parse(newValue);
        this.filteredData = [...this.data];
        this.currentPage = 1;
        this.render();
      } catch (error) {
        console.error("Error al analizar el JSON:", error);
        this.data = [];
        this.render();
      }
    }
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
          /* Estilos */
          .search-container {
            margin-bottom: 10px;
            display: flex;
            justify-content: center;
            align-items: center; /* Para alinear verticalmente el label y el input */
          }
          .search-container label {
            margin-right: 5px; /* Espacio entre el label y el input */
          }
          #searchInput {
            padding: 5px;
            border: 3px solid #000;
            border-radius: 4px;
            width: 200px;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            background-color: #fff;
          }
          th {
            background-color: #0a0a23;
            color: white;
            border-color: white;
          }
          /* Estilos para los botones */
          button {
            padding: 2px 10px;
            margin: 2px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
          }
  
          button:disabled {
            background-color: #cccccc;
            color: #666666;
            cursor: not-allowed;
          }
  
          button.devolver {
            background-color: red;
            color: white;
            font-weight: bold;
          }
          button.prestar {
            background-color: green;
            color: white;
            font-weight: bold;
          }
  
          /* Estilos hover */
          button:hover {
            opacity: 0.8;
          }
  
          .pagination {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            gap: 5px; /* Espacio entre los botones */
          }
          
          .pagination button {
            padding: 5px 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            background-color: #f0f0f0;
          }
          
          .pagination button:hover {
            background-color: #e0e0e0;
          }
          
          .pagination button.active {
            background-color: #007bff; /* Color azul para la página activa */
            color: white;
          }
          
          .pagination button:disabled {
            background-color: #f0f0f0;
            color: #999;
            cursor: not-allowed;
            border-color: #ccc;
          }
  
        </style>
        ${this.getSearchTemplate()}
        ${this.getTableTemplate()}
        ${this.getPaginationTemplate()}
      `;

    // Asociar el evento de input al elemento searchInput
    const searchInput = this.shadowRoot.getElementById("searchInput");
    if (searchInput) {
      // Eliminar el event listener anterior si existe
      searchInput.oninput = null;

      searchInput.addEventListener("input", (event) => {
        this.searchTerm = event.target.value;
        this.filterData(this.searchTerm);
      });

      // Poner el foco y cursor al final del input si hay datos
      
    }
  }

  getSearchTemplate() {
    return `<div class="search-container">
        <label for="searchInput">Buscar/Filtrar:</label>
        <input type="text" id="searchInput" placeholder="Buscar libro..." value="${this.searchTerm}">
      </div>`;
  }

  getPaginationTemplate() {
    const totalPages = Math.ceil(this.filteredData.length / this.itemsPerPage);
    if (totalPages <= 1) {
      return ""; // No mostrar paginación si hay una sola página o ninguna
    }
    let pagination = '<div class="pagination">';
    pagination += `<button id="prevPage" ${
      this.currentPage === 1 ? "disabled" : ""
    }>Anterior</button>`;
    for (let i = 1; i <= totalPages; i++) {
      pagination += `<button class="page-number ${
        this.currentPage === i ? "active" : ""
      }" data-page="${i}">${i}</button>`;
    }
    pagination += `<button id="nextPage" ${
      this.currentPage === totalPages ? "disabled" : ""
    }>Siguiente</button>`;
    pagination += "</div>";

    // Agregar los event listeners después de que el template se haya renderizado
    setTimeout(() => {
      this.shadowRoot.querySelectorAll(".page-number").forEach((button) => {
        button.addEventListener("click", () => {
          this.currentPage = parseInt(button.dataset.page);
          this.render();
        });
      });
      this.shadowRoot
        .getElementById("prevPage")
        .addEventListener("click", () => {
          if (this.currentPage > 1) {
            this.currentPage--;
            this.render();
          }
        });
      this.shadowRoot
        .getElementById("nextPage")
        .addEventListener("click", () => {
          if (this.currentPage < totalPages) {
            this.currentPage++;
            this.render();
          }
        });
    }, 0);
    return pagination;
  }

  getTableTemplate() {
    let tableRows = "";
    //Comprobar si el json que recibe tiene un mensaje.
    if (this.data.hasOwnProperty("message")) {
      tableRows = `<tr><td colspan="6">${this.data.message}</td></tr>`;
    } else if (this.filteredData.length === 0) {
      tableRows = `<tr><td colspan="6">Sin Resultados</td></tr>`;
    } else {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      const currentData = this.filteredData.slice(startIndex, endIndex);

      tableRows = currentData
        .map(
          (item, index) => `
        <tr>
          <td>${item.id}</td>
          <td>${item.autor}</td>
          <td>${item.titulo}</td>
          <td>${item.isbn}</td>
          <td>${item.disponible ? "Disponible" : "No Disponible"}</td>
          <td>
            <button class="devolver" ${
              item.disponible ? "disabled" : ""
            } onclick="devolverLibro(${item.id})">Devolver</button>
            <button class="prestar" ${
              item.disponible ? "" : "disabled"
            } onclick="prestarLibro(${item.id})">Prestar</button>
          </td>
        </tr>
      `
        )
        .join("");
    }

    return `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Autor</th>
            <th>Título</th>
            <th>ISBN</th>
            <th>Disponibilidad</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows}
        </tbody>
      </table>
    `;
  }

  filterData(searchTerm) {
    this.currentPage = 1;
    if (searchTerm.trim() === "") {
      this.filteredData = [...this.data];
    } else {
      this.filteredData = this.data.filter((item) => {
        const lowerSearchTerm = searchTerm.toLowerCase();
        const isbnWithoutDashes = item.isbn.replace(/-/g, ""); // Elimina los guiones del ISBN
        return (
          item.titulo.toLowerCase().includes(lowerSearchTerm) ||
          item.autor.toLowerCase().includes(lowerSearchTerm) ||
          isbnWithoutDashes.includes(lowerSearchTerm) // Compara sin guiones
        );
      });
    }

    this.render();
       // Obtener el campo de busqueda despues del render.
    const searchInput = this.shadowRoot.getElementById("searchInput");
    // Poner el foco y cursor al final del input si hay datos
    if (searchInput) {
        searchInput.focus();
        searchInput.setSelectionRange(
        searchInput.value.length,
        searchInput.value.length
      );
    }
  }
}

customElements.define("tabla-libros", TablaLibros);

async function listarLibros() {
  try {
    const response = await fetch("/listar");
    if (!response.ok) {
      throw new Error(`Error HTTP! estado: ${response.status}`);
    }
    const data = await response.json();
    //Seleccionar el web component que ya fue creado en el html.
    const tabla = document.querySelector("tabla-libros");
    //Añadir el atributo data al web component.
    tabla.setAttribute("data", JSON.stringify(data));
  } catch (error) {
    console.error("Error al obtener la lista de libros:", error);
  }
}

async function prestarLibro(id) {
  try {
    const response = await fetch(`/prestar/${id}`);
    if (!response.ok) {
      throw new Error(`Error HTTP! estado: ${response.status}`);
    }
    const data = await response.json();    
    //Comprobar si la operacion ha tenido exito.
    if (data.success) {
      mostrarToast(data.message);
    } else {
      console.error(data.message);
    }
    //Actualizar la tabla
    listarLibros();
  } catch (error) {
    console.error("Error al prestar el libro:", error);
  }
}

async function devolverLibro(id) {
  try {
    const response = await fetch(`/devolver/${id}`);
    if (!response.ok) {
      throw new Error(`Error HTTP! estado: ${response.status}`);
    }
    const data = await response.json();    
    //Comprobar si la operacion ha tenido exito.
    if (data.success) {
      mostrarToast(data.message);
    } else {
      console.error(data.message);
    }
    //Actualizar la tabla
    listarLibros();
  } catch (error) {
    console.error("Error al devolver el libro:", error);
  }
}

function mostrarCanvas() {
  const canvas = document.getElementById("myCanvas");
  canvas.style.display = "block"; // Aseguramos que el canvas sea visible

  // Aplicamos los estilos para simular el offcanvas-end de Bootstrap
  canvas.style.position = "fixed"; // Posición fija
  canvas.style.top = "0";
  canvas.style.right = "0";
  canvas.style.width = "300px"; // Ancho del offcanvas (puedes ajustarlo)
  canvas.style.height = "100%"; // Altura completa de la pantalla
  canvas.style.backgroundColor = "#fff"; // Fondo blanco
  canvas.style.boxShadow = "-2px 0px 5px rgba(0, 0, 0, 0.3)"; // Sombra lateral
  canvas.style.transition = "transform 0.3s ease-in-out"; // Transición suave
  canvas.style.zIndex = "1050"; // Asegurarse de que esté por encima de otros elementos
  canvas.style.transform = "translateX(0%)"; // Mostrar desde la derecha

  //Para que haga el movimiento de derecha a izquierda
  const body = document.body;
  body.style.transition = "margin-left 0.3s ease-in-out";
  body.style.marginLeft = "-300px";

  //Ocultar el scroll
  body.style.overflow = "hidden";
}

function ocultarCanvas() {
  const canvas = document.getElementById("myCanvas");
  canvas.style.transform = "translateX(100%)"; // Desplaza el canvas fuera de la vista a la derecha

  const body = document.body;
  body.style.marginLeft = "0px"; // Devuelve el body a su posición original
  body.style.overflow = "auto"; // Muestra el scroll del body

  // Espera a que la animación termine para ocultar el canvas completamente
  setTimeout(() => {
    canvas.style.display = "none";
  }, 300); // 300ms es la duración de la transición, debe coincidir
}


document.addEventListener('DOMContentLoaded', function() {
  const formulario = document.getElementById('myForm');
  const botonGuardar = document.getElementById('guardarLibro');

  botonGuardar.addEventListener('click', function(event) {
    event.preventDefault(); // Evita la recarga de la página
    const formData = new FormData(formulario);
    // Envia los datos al API
    async function guardarLibro() {
      try {
        const data = Object.fromEntries(formData.entries());
        const response = await fetch("/guardar", {
          method: "POST",
          body: formData,
        });
        if (!response.ok) {
          throw new Error(`Error HTTP! estado: ${response.status}`);
        }
        const dataResponse = await response.json();        
        //Comprobar si la operacion ha tenido exito.
        ocultarCanvas()
        if (dataResponse.success) {                    
          listarLibros();
          formulario.reset()
        }
        mostrarToast(dataResponse.message);          
      } catch (error) {
        console.error("Error al guardar el libro:", error);
      }
    }
    guardarLibro();
  });
});


async function buscarLibroPorIsbn(isbn) {  
  try {    
    const response = await fetch(`/buscar/${isbn}`);    
    if (!response.ok) {
      throw new Error(`Error HTTP! estado: ${response.status}`);
    }    
    const data = await response.json();        
    if (data.success) {            
      document.getElementById("autor").value = data.autor;
      document.getElementById("titulo").value = data.titulo;
      const selectDisponible = document.getElementById("disponible");
      selectDisponible.value = data.disponible ? "true" : "false";
    }
  } catch (error) {
    mostrarToast("Error al buscar el libro:", error);
  }
}

function buscarLibroPorIsbnEvent(event) {
  const isbnInput = event.target;
  const isbn = isbnInput.value;
  if (isbn.trim() !== "") {
    buscarLibroPorIsbn(isbn);
  }
}

function mostrarToast(texto) {
  // Crear el contenedor del toast
  const toastContainer = document.createElement("div");
  toastContainer.style.position = "fixed";
  toastContainer.style.top = "20px";
  toastContainer.style.right = "20px";
  toastContainer.style.backgroundColor = "#333";
  toastContainer.style.color = "#fff";
  toastContainer.style.padding = "15px";
  toastContainer.style.borderRadius = "5px";
  toastContainer.style.zIndex = "2000";
  toastContainer.style.opacity = "0";
  toastContainer.style.transition = "opacity 0.5s ease-in-out";
  toastContainer.style.boxShadow = "0 4px 8px rgba(229, 231, 235, 0.8)";
  

  // Crear el texto del toast
  const toastText = document.createElement("p");
  toastText.textContent = texto;
  toastText.style.margin = "0";

  // Crear la barra de progreso
  const progressBar = document.createElement("div");
  progressBar.style.width = "0%";
  progressBar.style.height = "5px";
  progressBar.style.backgroundColor = "green";
  progressBar.style.transition = "width 3s linear";
  progressBar.style.marginTop = "10px";

  // Añadir el texto y la barra al contenedor
  toastContainer.appendChild(toastText);
  toastContainer.appendChild(progressBar);

  // Añadir el contenedor al body
  document.body.appendChild(toastContainer);

  // Mostrar el toast
  setTimeout(() => {
    toastContainer.style.opacity = "1";
    progressBar.style.width = "100%";
  }, 100);

  // Ocultar el toast después de 3 segundos
  setTimeout(() => {
    toastContainer.style.opacity = "0";
    setTimeout(() => {
      document.body.removeChild(toastContainer);
    }, 500);
  }, 3000);
}

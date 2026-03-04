// Función que obtiene todos los productos desde el backend
// y los muestra en una tabla en la página.
function getProducts() {

    // Se hace una petición HTTP al microservicio de productos
    // para obtener la lista de productos.
    fetch('http://192.168.100.3:5003/api/products')

        // Cuando llega la respuesta, se convierte a formato JSON.
        .then(response => response.json())

        // "data" contiene el arreglo de productos que envía el backend.
        .then(data => {

            // Busca el cuerpo (tbody) de la tabla donde se mostrarán los productos.
            var productListBody = document.querySelector('#product-list tbody');

            // Limpia la tabla antes de llenarla nuevamente.
            productListBody.innerHTML = '';

            // Recorre cada producto recibido del backend.
            data.forEach(product => {

                // Crea una nueva fila en la tabla.
                var row = document.createElement('tr');

                // Inserta la información del producto en la fila.
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                    <td>${product.stock}</td>
                    <td>
                        <a href="/editProduct/${product.id}" class="btn btn-primary mr-2">Edit</a>
                        <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                    </td>
                `;

                // Agrega la fila a la tabla.
                productListBody.appendChild(row);
            });
        })

        // Si ocurre un error al hacer la petición.
        .catch(error => console.error('Error:', error));
}


// Función para crear un nuevo producto.
function createProduct() {

    // Se crea un objeto con la información del formulario.
    var data = {

        // Obtiene el valor del input "name".
        name: document.getElementById('name').value,

        // Obtiene el valor del input "description".
        description: document.getElementById('description').value,

        // Convierte el precio a número decimal.
        price: parseFloat(document.getElementById('price').value),

        // Convierte el stock a número entero.
        stock: parseInt(document.getElementById('stock').value)
    };

    // Envía una petición POST al backend para crear el producto.
    fetch('http://192.168.100.3:5003/api/products', {

        // Método HTTP POST (crear recurso).
        method: 'POST',

        // Indica que el contenido enviado es JSON.
        headers: { 'Content-Type': 'application/json' },

        // Convierte el objeto a JSON para enviarlo.
        body: JSON.stringify(data),
    })

    // Convierte la respuesta del servidor a JSON.
    .then(res => res.json())

    // Después de crear el producto, vuelve a cargar la lista de productos.
    .then(() => getProducts())

    // Si ocurre un error.
    .catch(error => console.error('Error:', error));
}


// Función para actualizar un producto existente.
function updateProduct() {

    // Obtiene el id del producto desde un input oculto.
    var productId = document.getElementById('product-id').value;

    // Se crea un objeto con la nueva información del producto.
    var data = {

        name: document.getElementById('name').value,

        description: document.getElementById('description').value,

        price: parseFloat(document.getElementById('price').value),

        stock: parseInt(document.getElementById('stock').value)
    };

    // Envía una petición PUT al backend para actualizar el producto.
    fetch(`http://192.168.100.3:5003/api/products/${productId}`, {

        // Método PUT (actualizar recurso).
        method: 'PUT',

        // Indica que el contenido enviado es JSON.
        headers: { 'Content-Type': 'application/json' },

        // Convierte los datos a JSON.
        body: JSON.stringify(data),
    })

    // Convierte la respuesta a JSON.
    .then(res => res.json())

    // Después de actualizar el producto, redirige a la página de productos.
    .then(() => window.location.href = "/products")

    // Si ocurre un error.
    .catch(error => console.error('Error:', error));
}


// Función para eliminar un producto.
function deleteProduct(productId) {

    // Muestra un mensaje de confirmación antes de eliminar.
    if (!confirm('Are you sure you want to delete this product?')) return;

    // Envía una petición DELETE al backend para eliminar el producto.
    fetch(`http://192.168.100.3:5003/api/products/${productId}`, {

        // Método HTTP DELETE.
        method: 'DELETE',
    })

    // Después de eliminar el producto, vuelve a cargar la lista.
    .then(() => getProducts())

    // Si ocurre un error.
    .catch(error => console.error('Error:', error));
}
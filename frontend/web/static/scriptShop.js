// Dirección del microservicio de productos.
// Desde aquí el frontend pedirá la lista de productos disponibles.
const PRODUCTS_BASE = "http://192.168.100.3:5003";

// Dirección del microservicio de usuarios.
// Se usa principalmente para cerrar sesión.
const USERS_BASE = "http://192.168.100.3:5002";

// Clave que se usará en localStorage para guardar el carrito.
const CART_KEY = "cart_items";


// Función para mostrar mensajes de alerta en la página
// (éxito, error, advertencia, etc.)
function showAlert(type, message) {

  // Busca el contenedor donde se mostrarán las alertas.
  const alertBox = document.getElementById("alertBox");

  // Si no existe el elemento, la función termina.
  if (!alertBox) return;

  // Inserta una alerta con estilos de Bootstrap.
  alertBox.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `;
}


// Función que obtiene el carrito guardado en el navegador.
function getCart() {

  try {

    // localStorage guarda datos como texto,
    // por eso usamos JSON.parse para convertirlo a objeto/arreglo.
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];

  } catch {

    // Si ocurre un error al leer el carrito,
    // se devuelve un carrito vacío.
    return [];
  }
}


// Función para guardar el carrito en localStorage.
function setCart(cart) {

  // Convierte el carrito a texto JSON y lo guarda.
  localStorage.setItem(CART_KEY, JSON.stringify(cart));

  // Actualiza el número de productos mostrado en el ícono del carrito.
  updateCartCount();
}


// Función que actualiza el contador del carrito en la interfaz.
function updateCartCount() {

  // Obtiene el carrito actual.
  const cart = getCart();

  // Suma la cantidad total de productos en el carrito.
  const count = cart.reduce((acc, it) => acc + (Number(it.quantity) || 0), 0);

  // Busca el elemento donde se muestra el contador.
  const el = document.getElementById("cartCount");

  // Si existe, actualiza el texto.
  if (el) el.textContent = String(count);
}


// Función para agregar un producto al carrito.
function addToCart(product, quantity) {

  // Convierte la cantidad a número.
  const qty = Number(quantity);

  // Verifica que la cantidad sea válida.
  if (!Number.isFinite(qty) || qty <= 0) {

    showAlert("warning", "Please enter a valid quantity (> 0).");
    return;
  }

  // Verifica que no se supere el stock disponible.
  if (qty > product.stock) {

    showAlert("warning", `Not enough stock. Available: ${product.stock}`);
    return;
  }

  // Obtiene el carrito actual.
  const cart = getCart();

  // Busca si el producto ya existe en el carrito.
  const idx = cart.findIndex((it) => it.id === product.id);

  // Si el producto ya estaba en el carrito:
  if (idx >= 0) {

    // Calcula la nueva cantidad.
    const newQty = Number(cart[idx].quantity) + qty;

    // Verifica que no supere el stock.
    if (newQty > product.stock) {

      showAlert("warning", `Cart quantity exceeds stock. Available: ${product.stock}`);
      return;
    }

    // Actualiza la cantidad del producto.
    cart[idx].quantity = newQty;

  } else {

    // Si el producto no estaba en el carrito,
    // se agrega como nuevo.
    cart.push({
      id: product.id,
      name: product.name,
      price: Number(product.price),
      quantity: qty,
    });
  }

  // Guarda el carrito actualizado.
  setCart(cart);

  // Muestra mensaje de éxito.
  showAlert("success", `Added "${product.name}" (x${qty}) to cart.`);
}


// Función que genera el HTML de una tarjeta de producto.
function productCard(product) {

  // Obtiene el stock del producto.
  const stock = Number(product.stock) || 0;

  // Crea una etiqueta visual dependiendo del stock.
  const stockBadge =
    stock > 0
      ? `<span class="badge badge-success stock-badge">In stock: ${stock}</span>`
      : `<span class="badge badge-danger stock-badge">Out of stock</span>`;

  // Devuelve el HTML de la tarjeta del producto.
  return `
    <div class="col-md-6 col-lg-4 mb-3">
      <div class="p-3 product-card h-100">

        <h5>${product.name}</h5>

        <p class="text-muted mb-2">${product.description || ""}</p>

        <div class="d-flex justify-content-between align-items-center mb-2">
          <strong>$${Number(product.price).toFixed(2)}</strong>
          ${stockBadge}
        </div>

        <div class="form-row align-items-center">

          <div class="col-5">
            <input
              type="number"
              min="1"
              class="form-control form-control-sm qty-input"
              placeholder="Qty"
              ${stock <= 0 ? "disabled" : ""}
            />
          </div>

          <div class="col">
            <button class="btn btn-primary btn-sm btn-add" ${stock <= 0 ? "disabled" : ""}>
              Add to cart
            </button>
          </div>

        </div>
      </div>
    </div>
  `;
}


// Función que carga los productos desde el backend.
async function loadProducts() {

  // Contenedor donde se mostrarán las tarjetas de productos.
  const grid = document.getElementById("productsGrid");

  // Limpia el contenedor antes de cargar productos nuevos.
  grid.innerHTML = "";

  try {

    // Hace una petición al microservicio de productos.
    const res = await fetch(`${PRODUCTS_BASE}/api/products`);

    // Convierte la respuesta a JSON.
    const data = await res.json();

    // Si ocurre un error al cargar productos.
    if (!res.ok) {
      showAlert("danger", "Could not load products.");
      return;
    }

    // Si no hay productos disponibles.
    if (!Array.isArray(data) || data.length === 0) {
      showAlert("info", "No products found.");
      return;
    }

    // Genera todas las tarjetas de productos.
    grid.innerHTML = data.map(productCard).join("");

    // --------------------------
    // EVENTOS PARA LOS BOTONES
    // --------------------------

    const cards = Array.from(grid.querySelectorAll(".product-card"));

    cards.forEach((card, i) => {

      const product = data[i];

      const input = card.querySelector(".qty-input");

      const btn = card.querySelector(".btn-add");

      btn.addEventListener("click", () => {

        // Agrega el producto al carrito.
        addToCart(product, input.value || 1);

        // Limpia el campo de cantidad.
        input.value = "";
      });
    });

  } catch (err) {

    console.error(err);

    showAlert("danger", "Network error while loading products.");
  }
}


// Función para cerrar sesión.
async function logout() {

  // Intenta cerrar sesión en el backend.
  try {

    await fetch(`${USERS_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",
    });

  } catch (_) {}

  // Elimina datos del usuario guardados en el navegador.
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  localStorage.removeItem("email");

  // El carrito NO se borra automáticamente (opcional).
  // Si se quisiera borrar también:
  // localStorage.removeItem(CART_KEY);

  // Redirige a la página principal.
  window.location.href = "/";
}


// Este evento se ejecuta cuando el HTML termina de cargar.
document.addEventListener("DOMContentLoaded", () => {

  // Actualiza el contador del carrito.
  updateCartCount();

  // Carga los productos desde el backend.
  loadProducts();

  // Botón para refrescar productos manualmente.
  document.getElementById("btnRefresh").addEventListener("click", loadProducts);

  // Botón para cerrar sesión.
  document.getElementById("btnLogout").addEventListener("click", logout);
});
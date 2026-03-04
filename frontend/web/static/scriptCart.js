// Dirección del microservicio que maneja las órdenes (pedidos).
// Aquí se enviarán las solicitudes para crear una orden.
const ORDERS_BASE = "http://192.168.100.3:5004";

// Dirección del microservicio de usuarios.
// Se usa para acciones como cerrar sesión.
const USERS_BASE = "http://192.168.100.3:5002";

// Nombre de la clave que se usará en localStorage para guardar el carrito.
const CART_KEY = "cart_items";


// Función para mostrar mensajes de alerta en la página
// (por ejemplo errores, advertencias o mensajes de éxito).
function showAlert(type, message) {

  // Busca en el HTML un elemento con id "alertBox".
  const alertBox = document.getElementById("alertBox");

  // Si no existe ese elemento, la función termina.
  if (!alertBox) return;

  // Inserta dentro del alertBox una alerta de Bootstrap.
  // "type" define el color de la alerta (success, danger, warning, etc).
  // "message" es el texto que se quiere mostrar.
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
    // por eso se usa JSON.parse para convertirlo a objeto o arreglo.
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];

  } catch {

    // Si ocurre un error al leer los datos, devuelve un carrito vacío.
    return [];
  }
}


// Función para guardar el carrito en localStorage.
function setCart(cart) {

  // Convierte el carrito (objeto/arreglo) a texto JSON
  // y lo guarda en el navegador.
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}


// Función que calcula el total del carrito.
function calcTotal(cart) {

  // reduce recorre todos los productos del carrito
  // y va acumulando el total.
  return cart.reduce((acc, it) => acc + (Number(it.price) || 0) * (Number(it.quantity) || 0), 0);
}


// Función que dibuja el carrito en la tabla HTML.
function renderCart() {

  // Busca el cuerpo (tbody) de la tabla del carrito.
  const tbody = document.querySelector("#cartTable tbody");

  // Obtiene los productos guardados en el carrito.
  const cart = getCart();

  // Limpia la tabla antes de volver a dibujarla.
  tbody.innerHTML = "";

  // Si el carrito está vacío:
  if (cart.length === 0) {

    // Muestra un mensaje indicando que el carrito está vacío.
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="text-center text-muted">Your cart is empty.</td>
      </tr>
    `;

    // El total se pone en 0.
    document.getElementById("cartTotal").textContent = "0.00";

    return;
  }

  // Recorre todos los productos del carrito.
  cart.forEach((it, idx) => {

    // Crea una nueva fila de tabla.
    const tr = document.createElement("tr");

    // Calcula el subtotal del producto (precio × cantidad).
    const subtotal = (Number(it.price) || 0) * (Number(it.quantity) || 0);

    // Inserta el contenido de la fila.
    tr.innerHTML = `
      <td>${it.name}</td>
      <td>$${Number(it.price).toFixed(2)}</td>
      <td>
        <input class="form-control form-control-sm qty" type="number" min="1" value="${it.quantity}" data-idx="${idx}" />
      </td>
      <td>$${subtotal.toFixed(2)}</td>
      <td>
        <button class="btn btn-sm btn-danger" data-remove="${idx}">Remove</button>
      </td>
    `;

    // Agrega la fila a la tabla.
    tbody.appendChild(tr);
  });

  // Muestra el total del carrito.
  document.getElementById("cartTotal").textContent = calcTotal(cart).toFixed(2);


  // ------------------------------
  // EVENTOS PARA CAMBIAR CANTIDAD
  // ------------------------------

  tbody.querySelectorAll(".qty").forEach((input) => {

    input.addEventListener("change", (e) => {

      // Obtiene el índice del producto en el carrito.
      const idx = Number(e.target.dataset.idx);

      // Obtiene la nueva cantidad que escribió el usuario.
      const newQty = Number(e.target.value);

      // Si la cantidad no es válida:
      if (!Number.isFinite(newQty) || newQty <= 0) {

        showAlert("warning", "Quantity must be > 0");

        // Se vuelve a renderizar el carrito.
        renderCart();
        return;
      }

      // Obtiene el carrito actual.
      const cart = getCart();

      // Cambia la cantidad del producto.
      cart[idx].quantity = newQty;

      // Guarda el carrito actualizado.
      setCart(cart);

      // Vuelve a dibujar el carrito.
      renderCart();
    });
  });


  // ------------------------------
  // EVENTOS PARA ELIMINAR PRODUCTO
  // ------------------------------

  tbody.querySelectorAll("[data-remove]").forEach((btn) => {

    btn.addEventListener("click", (e) => {

      // Obtiene el índice del producto a eliminar.
      const idx = Number(e.target.dataset.remove);

      // Obtiene el carrito actual.
      const cart = getCart();

      // Elimina el producto del arreglo.
      cart.splice(idx, 1);

      // Guarda el carrito actualizado.
      setCart(cart);

      // Redibuja el carrito.
      renderCart();
    });
  });
}


// Función que construye el objeto que se enviará al backend
// para crear una orden.
function buildOrderPayload(cart) {

  return {
    products: cart.map((it) => ({

      // id del producto
      id: it.id,

      // cantidad del producto
      quantity: Number(it.quantity),

    })),
  };
}


// Función que genera una orden en el sistema.
async function generateOrder() {

  // Obtiene el carrito actual.
  const cart = getCart();

  // Si el carrito está vacío:
  if (cart.length === 0) {
    showAlert("warning", "Cart is empty.");
    return;
  }

  // Construye el objeto que se enviará al backend.
  const payload = buildOrderPayload(cart);

  try {

    // Envía la solicitud al microservicio de órdenes.
    const res = await fetch(`${ORDERS_BASE}/api/orders`, {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      credentials: "include", // IMPORTANT: session cookie

      body: JSON.stringify(payload),
    });

    const data = await res.json().catch(() => ({}));


    // ------------------------------
    // MANEJO DE ERRORES
    // ------------------------------

    if (res.status === 400) {
      showAlert("danger", data?.message || "Bad request. Maybe you are not logged in.");
      return;
    }

    if (res.status === 409) {
      showAlert("warning", data?.message || "Insufficient stock for one or more products.");
      return;
    }

    if (res.status === 503) {
      showAlert("danger", data?.message || "Products service unavailable (Consul). Try again later.");
      return;
    }

    if (!res.ok) {
      showAlert("danger", data?.message || "Could not create order.");
      return;
    }


    // ------------------------------
    // SI TODO SALE BIEN
    // ------------------------------

    const orderId = data?.order_id;

    showAlert("success", `Order created successfully! Order ID: ${orderId || "-"}`);

    // Muestra el resultado en pantalla.
    document.getElementById("orderResult").innerHTML = `
      <div class="alert alert-success">
        ✅ Order created. <strong>Order ID:</strong> ${orderId || "-"}
      </div>
    `;

    // Limpia el carrito después de crear la orden.
    localStorage.removeItem(CART_KEY);

    // Vuelve a dibujar el carrito (vacío).
    renderCart();

  } catch (err) {

    console.error(err);

    showAlert("danger", "Network error while creating order.");
  }
}


// Función para cerrar sesión del usuario.
async function logout() {

  try {

    // Envía una solicitud al backend para cerrar la sesión.
    await fetch(`${USERS_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",
    });

  } catch (_) {}

  // Elimina los datos del usuario guardados en el navegador.
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  localStorage.removeItem("email");

  // Redirige al usuario a la página principal.
  window.location.href = "/";
}


// Este evento se ejecuta cuando el HTML ya terminó de cargar.
document.addEventListener("DOMContentLoaded", () => {

  // Dibuja el carrito al cargar la página.
  renderCart();

  // Botón para generar orden.
  document.getElementById("btnOrder").addEventListener("click", generateOrder);

  // Botón para limpiar el carrito.
  document.getElementById("btnClear").addEventListener("click", () => {

    localStorage.removeItem(CART_KEY);

    renderCart();

    showAlert("info", "Cart cleared.");
  });

  // Botón para cerrar sesión.
  document.getElementById("btnLogout").addEventListener("click", logout);
});
// Dirección del microservicio que maneja las órdenes (pedidos).
// Aquí se enviarán las peticiones para consultar órdenes.
const ORDERS_BASE = "http://192.168.100.3:5004";

// Dirección del microservicio de usuarios.
// Se usa principalmente para cerrar sesión.
const USERS_BASE = "http://192.168.100.3:5002";


// Función para mostrar mensajes de alerta en la página.
// Sirve para mostrar errores, advertencias o mensajes de éxito.
function showAlert(type, message) {

  // Busca el elemento HTML donde se mostrarán las alertas.
  const alertBox = document.getElementById("alertBox");

  // Inserta un mensaje con estilos de Bootstrap.
  // type = color de alerta (success, danger, warning, etc.)
  // message = texto que se mostrará.
  alertBox.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
    </div>
  `;
}


// Función que convierte un número a formato de dinero.
function money(v) {

  // Convierte el valor recibido a número.
  // Si no es válido, usa 0.
  const n = Number(v) || 0;

  // Devuelve el número con dos decimales y el símbolo $.
  return `$${n.toFixed(2)}`;
}


// Función para obtener el username del usuario que inició sesión.
function getLoggedUsername() {

  // Busca el username guardado en localStorage.
  // trim() elimina espacios al inicio y al final.
  return (localStorage.getItem("username") || "").trim();
}


// Función que carga las órdenes del usuario actual.
async function loadMyOrders() {

  // Obtiene el username del usuario logueado.
  const username = getLoggedUsername();

  // Si no hay username guardado:
  if (!username) {

    // Muestra advertencia.
    showAlert("warning", "No username found in localStorage. Please login again.");

    return;
  }

  // Busca el cuerpo de la tabla donde se mostrarán las órdenes.
  const tbody = document.querySelector("#ordersTable tbody");

  // Limpia la tabla antes de agregar datos nuevos.
  tbody.innerHTML = "";

  try {

    // En este enfoque del frontend:
    // se traen TODAS las órdenes y luego se filtran.
    const res = await fetch(`${ORDERS_BASE}/api/orders`, {
      credentials: "include",
    });

    // Convierte la respuesta a JSON.
    const data = await res.json().catch(() => []);

    // Si el backend devuelve error de sesión:
    if (res.status === 400) {
      showAlert("danger", data?.message || "Not logged in. Please login again.");
      return;
    }

    // Si ocurre otro error:
    if (!res.ok) {
      showAlert("danger", data?.message || "Could not load orders.");
      return;
    }

    // Filtra solo las órdenes que pertenecen al usuario actual.
    const myOrders = (Array.isArray(data) ? data : []).filter(
      (o) => String(o.user_name || "").trim() === username
    );

    // Si el usuario no tiene órdenes:
    if (myOrders.length === 0) {
      showAlert("info", `No orders found for "${username}".`);
      return;
    }

    // Recorre todas las órdenes del usuario.
    myOrders.forEach((o) => {

      // Crea una nueva fila en la tabla.
      const tr = document.createElement("tr");

      // Inserta los datos de la orden.
      tr.innerHTML = `
        <td>${o.id}</td>
        <td>${money(o.total)}</td>
        <td>${o.created_at || "-"}</td>
        <td><button class="btn btn-sm btn-primary" data-view="${o.id}">View items</button></td>
      `;

      // Agrega la fila a la tabla.
      tbody.appendChild(tr);
    });

    // Busca todos los botones "View items".
    tbody.querySelectorAll("[data-view]").forEach((btn) => {

      // Cuando se presione el botón,
      // se mostrará el detalle de la orden.
      btn.addEventListener("click", () => viewOrder(btn.dataset.view));
    });

    // Muestra mensaje de éxito indicando cuántas órdenes se cargaron.
    showAlert("success", `Loaded ${myOrders.length} orders for ${username}.`);

  } catch (err) {

    // Si ocurre un error de red.
    console.error(err);

    showAlert("danger", "Network error while loading orders.");
  }
}


// Función que muestra los detalles de una orden específica.
async function viewOrder(orderId) {

  // Busca el contenedor donde se mostrarán los detalles.
  const box = document.getElementById("orderDetails");

  // Muestra un mensaje temporal mientras se cargan los datos.
  box.innerHTML = "Loading...";

  try {

    // Hace una petición al backend para obtener los detalles de una orden.
    const res = await fetch(`${ORDERS_BASE}/api/orders/${orderId}`, {
      credentials: "include",
    });

    const data = await res.json().catch(() => ({}));

    // Si ocurre un error:
    if (!res.ok) {

      // Muestra el error en el modal.
      box.innerHTML = `<div class="alert alert-danger">${data?.message || "Could not load order."}</div>`;

      // Abre el modal.
      $("#orderModal").modal("show");

      return;
    }

    // Obtiene los productos de la orden.
    const items = data.items || data.order_items || [];

    // Construye las filas de la tabla de productos.
    const itemsRows = Array.isArray(items) && items.length
      ? items.map((it) => `
          <tr>
            <td>${it.product_id ?? it.productId ?? "-"}</td>
            <td>${it.quantity ?? "-"}</td>
            <td>${money(it.price)}</td>
            <td>${money((Number(it.price)||0) * (Number(it.quantity)||0))}</td>
          </tr>
        `).join("")
      : `<tr><td colspan="4" class="text-center text-muted">No items</td></tr>`;


    // Construye el contenido HTML del modal con los detalles de la orden.
    box.innerHTML = `
      <div class="mb-2">
        <strong>Order #${data.id}</strong>
        <div class="text-muted">${data.created_at || ""}</div>
      </div>

      <div class="table-responsive">
        <table class="table table-sm table-striped">
          <thead>
            <tr>
              <th>Product ID</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>${itemsRows}</tbody>
        </table>
      </div>

      <div class="d-flex justify-content-end">
        <h5>Total: ${money(data.total)}</h5>
      </div>
    `;

    // Muestra el modal con los detalles de la orden.
    $("#orderModal").modal("show");

  } catch (err) {

    console.error(err);

    // Si ocurre un error de red.
    box.innerHTML = `<div class="alert alert-danger">Network error while loading order details.</div>`;

    $("#orderModal").modal("show");
  }
}


// Función para cerrar sesión del usuario.
async function logout() {

  try {

    // Envía una petición al backend para cerrar la sesión.
    await fetch(`${USERS_BASE}/api/logout`, { method: "POST", credentials: "include" });

  } catch (_) {}

  // Elimina los datos del usuario guardados en el navegador.
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  localStorage.removeItem("email");

  // Redirige al usuario a la página principal.
  window.location.href = "/";
}


// Este evento se ejecuta cuando la página HTML termina de cargar.
document.addEventListener("DOMContentLoaded", () => {

  // Botón para recargar las órdenes del usuario.
  document.getElementById("btnRefresh").addEventListener("click", loadMyOrders);

  // Botón para cerrar sesión.
  document.getElementById("btnLogout").addEventListener("click", logout);

  // Carga automáticamente las órdenes del usuario al abrir la página.
  loadMyOrders();
});
// Dirección del microservicio que maneja las órdenes.
// Aquí se enviarán las peticiones para consultar pedidos.
const ORDERS_BASE = "http://192.168.100.3:5004";


// Función para mostrar mensajes de alerta en la página.
// Se usa para informar errores, advertencias o mensajes de éxito.
function showAlert(type, message) {

  // Busca el elemento del HTML donde se mostrarán las alertas.
  const alertBox = document.getElementById("alertBox");

  // Inserta dentro del alertBox un mensaje con estilo de Bootstrap.
  // type puede ser: success, danger, warning, info, etc.
  // message es el texto que se mostrará.
  alertBox.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
    </div>
  `;
}


// Función para formatear números como dinero.
function money(v) {

  // Convierte el valor recibido a número.
  // Si no se puede convertir, usa 0.
  const n = Number(v) || 0;

  // toFixed(2) asegura que el número tenga 2 decimales.
  // Se agrega el símbolo "$".
  return `$${n.toFixed(2)}`;
}


// Función que carga las órdenes desde el backend
// y las muestra en una tabla.
async function loadOrders() {

  // Busca el cuerpo (tbody) de la tabla de órdenes.
  const tbody = document.querySelector("#ordersTable tbody");

  // Limpia la tabla antes de llenarla con datos nuevos.
  tbody.innerHTML = "";

  try {

    // Hace una petición al backend para obtener todas las órdenes.
    const res = await fetch(`${ORDERS_BASE}/api/orders`, {

      // Permite enviar cookies de sesión si el backend las necesita.
      credentials: "include",
    });

    // Intenta convertir la respuesta a JSON.
    const data = await res.json().catch(() => []);

    // Si el servidor responde con error:
    if (!res.ok) {
      showAlert("danger", data?.message || "Could not load orders.");
      return;
    }

    // Si no hay órdenes en el sistema:
    if (!Array.isArray(data) || data.length === 0) {
      showAlert("info", "No orders found.");
      return;
    }

    // Recorre todas las órdenes recibidas.
    data.forEach((o) => {

      // Crea una fila nueva en la tabla.
      const tr = document.createElement("tr");

      // Inserta los datos de la orden en la fila.
      tr.innerHTML = `
        <td>${o.id}</td>
        <td>${o.user_name || "-"}</td>
        <td>${o.user_email || "-"}</td>
        <td>${money(o.total)}</td>
        <td>${o.created_at || "-"}</td>
        <td>
          <button class="btn btn-sm btn-primary" data-view="${o.id}">View items</button>
        </td>
      `;

      // Agrega la fila a la tabla.
      tbody.appendChild(tr);
    });

    // Busca todos los botones "View items".
    tbody.querySelectorAll("[data-view]").forEach((btn) => {

      // Cuando se presione el botón, se mostrará el detalle de la orden.
      btn.addEventListener("click", () => viewOrder(btn.dataset.view));
    });

    // Muestra un mensaje indicando cuántas órdenes se cargaron.
    showAlert("success", `Loaded ${data.length} orders.`);

  } catch (err) {

    // Si ocurre un error de red (por ejemplo el servidor no responde).
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

    // Hace una petición al backend para obtener una orden específica.
    const res = await fetch(`${ORDERS_BASE}/api/orders/${orderId}`, {
      credentials: "include",
    });

    const data = await res.json().catch(() => ({}));

    // Si ocurre un error al obtener la orden:
    if (!res.ok) {

      // Muestra el error dentro del modal.
      box.innerHTML = `<div class="alert alert-danger">${data?.message || "Could not load order."}</div>`;

      // Abre el modal.
      $("#orderModal").modal("show");

      return;
    }

    // Se espera que el backend devuelva algo como:
    // { id, user_name, total, created_at, items:[...] }

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

      // Si la orden no tiene productos:
      : `<tr><td colspan="4" class="text-center text-muted">No items</td></tr>`;


    // Construye todo el contenido HTML del modal.
    box.innerHTML = `

      <div class="mb-2">
        <strong>Order #${data.id}</strong> — ${data.user_name || "-"} (${data.user_email || "-"})
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


// Este evento se ejecuta cuando el HTML termina de cargar.
document.addEventListener("DOMContentLoaded", () => {

  // Botón para actualizar la lista de órdenes.
  document.getElementById("btnRefresh").addEventListener("click", loadOrders);

  // Carga las órdenes automáticamente al abrir la página.
  loadOrders();
});
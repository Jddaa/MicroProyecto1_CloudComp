// Esta constante guarda la dirección del microservicio de usuarios.
// Es la URL base a donde se enviarán las peticiones de login.
const USERS_BASE = "http://192.168.100.3:5002";


// Esta función sirve para mostrar mensajes de alerta en la página.
// Por ejemplo: errores, éxito al iniciar sesión, etc.
function showAlert(type, message) {

  // Busca en el HTML un elemento con id "alertBox"
  // Aquí se van a mostrar los mensajes.
  const alertBox = document.getElementById("alertBox");

  // Si no existe el elemento en la página, la función se detiene.
  if (!alertBox) return;

  // Se inserta HTML dentro del alertBox para mostrar una alerta de Bootstrap.
  // "type" define el color (success, danger, warning, etc).
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


// Este evento se ejecuta cuando todo el HTML de la página ya se cargó.
document.addEventListener("DOMContentLoaded", () => {

  // Busca el formulario de login en la página (id="loginForm")
  const form = document.getElementById("loginForm");

  // Si no existe el formulario, no hace nada.
  if (!form) return;

  // Se agrega un "escuchador de evento" al formulario.
  // Esto detecta cuando el usuario presiona el botón de enviar (submit).
  form.addEventListener("submit", async (e) => {

    // Evita que el formulario recargue la página automáticamente.
    e.preventDefault();

    // Obtiene el valor del input donde el usuario escribe su username.
    // trim() elimina espacios al inicio y al final.
    const username = document.getElementById("loginUsername").value.trim();

    // Obtiene el valor del input de la contraseña.
    const password = document.getElementById("loginPassword").value;

    try {

      // Aquí se hace una petición HTTP al backend usando fetch.
      // Se envía la información del login al microservicio de usuarios.
      const res = await fetch(`${USERS_BASE}/api/login`, {

        // Método HTTP que se va a usar.
        method: "POST",

        // Indica que el contenido enviado es JSON.
        headers: { "Content-Type": "application/json" },

        // Permite enviar y recibir cookies de sesión.
        // Esto es importante para mantener al usuario autenticado.
        credentials: "include", // IMPORTANT: session cookie

        // Convierte el username y password a formato JSON para enviarlos.
        body: JSON.stringify({ username, password }),
      });

      // Intenta convertir la respuesta del servidor a JSON.
      // Si falla, devuelve un objeto vacío.
      const data = await res.json().catch(() => ({}));

      // Si la respuesta del servidor NO es correcta (ej: usuario incorrecto)
      if (!res.ok) {

        // Usa el mensaje que envíe el backend o un mensaje por defecto.
        const msg = data?.message || "Login failed. Check credentials.";

        // Muestra una alerta de error en la página.
        showAlert("danger", msg);

        // Termina la función.
        return;
      }

      // Si el login fue exitoso:

      // Guarda información básica del usuario en el navegador.
      // No es obligatorio, pero puede servir para mostrar datos del usuario.
      localStorage.setItem("role", "client");

      // Si el backend devolvió el username, se guarda.
      if (data?.username) localStorage.setItem("username", data.username);

      // Si el backend devolvió el email, se guarda.
      if (data?.email) localStorage.setItem("email", data.email);

      // Cierra el modal de login (ventana emergente) usando jQuery y Bootstrap.
      $("#loginModal").modal("hide");

      // Muestra una alerta de éxito indicando que el login fue correcto.
      showAlert("success", `Login OK. Welcome ${data.username || ""} — redirecting to shop...`);

      // Espera 400 milisegundos antes de redirigir al usuario.
      setTimeout(() => {

        // Redirige al usuario a la página de la tienda.
        window.location.href = "/shop";

      }, 400);

    } catch (err) {

      // Si ocurre un error de red (por ejemplo el servidor no responde)
      console.error(err);

      // Se muestra una alerta indicando que hubo un error de conexión.
      showAlert("danger", "Network error while logging in.");
    }
  });
});
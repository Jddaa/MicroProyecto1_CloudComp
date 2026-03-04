// Función que obtiene todos los usuarios desde el backend
// y los muestra en una tabla en la página.
function getUsers() {

  // Se hace una petición HTTP al microservicio de usuarios
  // para obtener la lista de usuarios.
  fetch("http://192.168.100.3:5002/api/users")

    // Convierte la respuesta del servidor a formato JSON.
    .then((response) => response.json())

    // "data" contiene el arreglo de usuarios que envía el backend.
    .then((data) => {

      // Imprime los usuarios en la consola (solo para depuración).
      console.log(data);

      // Busca el cuerpo (tbody) de la tabla donde se mostrarán los usuarios.
      var userListBody = document.querySelector("#user-list tbody");

      // Limpia cualquier contenido anterior de la tabla.
      userListBody.innerHTML = "";

      // Recorre cada usuario recibido del backend.
      data.forEach((user) => {

        // Crea una nueva fila de tabla.
        var row = document.createElement("tr");


        // -------------------
        // COLUMNA: NOMBRE
        // -------------------

        var nameCell = document.createElement("td");

        // Coloca el nombre del usuario.
        nameCell.textContent = user.name;

        // Agrega la celda a la fila.
        row.appendChild(nameCell);


        // -------------------
        // COLUMNA: EMAIL
        // -------------------

        var emailCell = document.createElement("td");

        emailCell.textContent = user.email;

        row.appendChild(emailCell);


        // -------------------
        // COLUMNA: USERNAME
        // -------------------

        var usernameCell = document.createElement("td");

        usernameCell.textContent = user.username;

        row.appendChild(usernameCell);


        // -------------------
        // COLUMNA: ACCIONES
        // -------------------

        var actionsCell = document.createElement("td");


        // BOTÓN / LINK PARA EDITAR

        var editLink = document.createElement("a");

        // Redirige a la página de edición del usuario.
        editLink.href = `/editUser/${user.id}`;

        // Alternativa que estaba comentada:
        // editLink.href = `edit.html?id=${user.id}`;

        editLink.textContent = "Edit";

        // Clases de Bootstrap para estilo.
        editLink.className = "btn btn-primary mr-2";

        actionsCell.appendChild(editLink);


        // BOTÓN / LINK PARA ELIMINAR

        var deleteLink = document.createElement("a");

        deleteLink.href = "#";

        deleteLink.textContent = "Delete";

        deleteLink.className = "btn btn-danger";

        // Cuando se haga clic, se ejecuta la función deleteUser.
        deleteLink.addEventListener("click", function () {
          deleteUser(user.id);
        });

        actionsCell.appendChild(deleteLink);


        // Agrega la columna de acciones a la fila.
        row.appendChild(actionsCell);

        // Agrega la fila completa a la tabla.
        userListBody.appendChild(row);
      });
    })

    // Si ocurre un error al hacer la petición.
    .catch((error) => console.error("Error:", error));
}



// Función para crear un nuevo usuario.
function createUser() {

  // Se crea un objeto con los datos del formulario.
  var data = {

    // Obtiene el valor del campo "name".
    name: document.getElementById("name").value,

    // Obtiene el valor del campo "email".
    email: document.getElementById("email").value,

    // Obtiene el valor del campo "username".
    username: document.getElementById("username").value,

    // Obtiene el valor del campo "password".
    password: document.getElementById("password").value,
  };


  // Envía una petición POST al backend para crear el usuario.
  fetch("http://192.168.100.3:5002/api/users", {

    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    // Convierte el objeto a JSON para enviarlo.
    body: JSON.stringify(data),
  })

    .then((response) => {

      // Si la respuesta del servidor no es correcta,
      // se lanza un error.
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      return response.json();
    })

    .then((data) => {

      console.log(data);

      // Refresca la lista de usuarios.
      getUsers();

      // Limpia el formulario después de crear el usuario.
      document.getElementById("name").value = "";
      document.getElementById("email").value = "";
      document.getElementById("username").value = "";
      document.getElementById("password").value = "";
    })

    .catch((error) => {

      // Manejo de errores.
      console.error("Error:", error);
    });
}



// Función para actualizar un usuario existente.
function updateUser() {

  // Obtiene el id del usuario desde un campo oculto.
  var userId = document.getElementById("user-id").value;

  // Se crea un objeto con los nuevos datos del usuario.
  var data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
  };


  // Envía una petición PUT al backend para actualizar el usuario.
  fetch(`http://192.168.100.3:5002/api/users/${userId}`, {

    method: "PUT",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(data),
  })

    .then((response) => {

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      return response.json();
    })

    .then((data) => {

      console.log(data);

      // Después de actualizar el usuario,
      // redirige a la página de usuarios.
      window.location.href = "/users";
    })

    .catch((error) => {

      console.error("Error:", error);
    });
}



// Función para eliminar un usuario.
function deleteUser(userId) {

  // Muestra en consola el ID del usuario que se va a eliminar.
  console.log("Deleting user with ID:", userId);

  // Muestra un mensaje de confirmación.
  if (confirm("Are you sure you want to delete this user?")) {

    // Envía una petición DELETE al backend.
    fetch(`http://192.168.100.3:5002/api/users/${userId}`, {

      method: "DELETE",
    })

      .then((response) => {

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        return response.json();
      })

      .then((data) => {

        // Mensaje en consola indicando que se eliminó correctamente.
        console.log("User deleted successfully:", data);

        // Recarga la lista de usuarios.
        getUsers();
      })

      .catch((error) => {

        console.error("Error:", error);
      });
  }
}
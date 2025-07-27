function obetenerToken() {
    const cookies = document.cookie.split(';');
    const tokenCookie = cookies.find(cookie => cookie.trim().startsWith('token='));
    if (tokenCookie) {
        return decodeURIComponent(tokenCookie.split('=')[1]);
    }
    return null;
}

function generarTablaUsuarios(){
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-usuarios/";
    if (token) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.estatus === 200) {
                let usuarios = data.data;
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre</th><th>Tipo Usuario</th><th>Estatus</th></tr></thead><tbody>';
                usuarios.forEach(usuario => {
                    let nombreCompleto = usuario.nombre + ' ' + usuario.paterno + ' ' + usuario.materno;
                    tabla += `<tr>
                        <td>${usuario.id_usuario}</td>
                        <td>${nombreCompleto}</td>
                        <td>${usuario.fk_id_cat_tipo_usuario__nombre}</td>
                        <td>${usuario.estatus ? 'Activo' : 'Inactivo'}</td>
                    </tr>`;
                });
                tabla += '</tbody></table>';
                document.getElementById('tablaUsuarios').innerHTML = tabla;
            } else {
                alert('Error al obtener los usuarios');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los usuarios');
        });
    } else {
        alert('No se encontró el token de acceso');
    }
}

function obtenerTiposUsuario() {
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-tipos-usuario/";
    if (token) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.estatus === 200) {
                let tiposUsuario = data.data;
                let select = document.getElementById('adminRole');
                select.innerHTML = '<option value="" disabled selected>Selecciona un rol</option>';
                tiposUsuario.forEach(tipo => {
                    select.innerHTML += `<option value="${tipo.id_tipo_usuario}">${tipo.nombre}</option>`;
                });
            } else {
                alert('Error al obtener los tipos de usuario');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los tipos de usuario');
        });
    } else {
        alert('No se encontró el token de acceso');
    }
}
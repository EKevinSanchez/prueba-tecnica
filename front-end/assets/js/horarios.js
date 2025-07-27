function obetenerToken() {
    const cookies = document.cookie.split(';');
    const tokenCookie = cookies.find(cookie => cookie.trim().startsWith('token='));
    if (tokenCookie) {
        return decodeURIComponent(tokenCookie.split('=')[1]);
    }
    return null;
}

let catalogo_horario_dias = [];
let catalogo_horario_horas = [];

function generarTablaHorarioDias() {
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-horario-dias/"
    if(token){
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
                let dias = data.data;
                catalogo_horario_dias = dias; // Guardar los días en el catálogo
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Día</th></tr></thead><tbody>';
                dias.forEach(dia => {
                    tabla += `<tr>
                        <td>${dia.id_cat_horario_dia}</td>
                        <td>${dia.dias}</td>
                    </tr>`;
                });
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-horario-dias').innerHTML = tabla;
            } else {
                alert('Error al obtener los días del horario');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los días del horario');
        });
    }
}

function generarTablaHorarioHoras() {
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-horario-horas/";
    if(token){
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
                let horas = data.data;
                catalogo_horario_horas = horas; // Guardar las horas en el catálogo
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Hora Inicio</th><th>Hora Fin</th></tr></thead><tbody>';
                horas.forEach(hora => {

                    tabla += `<tr>
                        <td>${hora.id_cat_horarios_hora}</td>
                        <td>${hora.hora_entrada}</td>
                        <td>${hora.hora_salida}</td>
                    </tr>`;
                });
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-horario-horas').innerHTML = tabla;
            } else {
                alert('Error al obtener las horas del horario');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener las horas del horario');
        });
    }
}

function generarTablaHorarioTrabajador(){
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-horario-trabajador/";
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
                let trabajadores = data.data;
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Trabajador</th><th>Día</th><th>Hora Inicio</th><th>Hora Fin</th></tr></thead><tbody>';
                trabajadores.forEach(trabajador => {
                    tabla += `<tr>
                        <td>${trabajador.id_trabajador}</td>
                        <td>${trabajador.nombre_trabajador}</td>
                        <td>${trabajador.dia_nombre}</td>
                        <td>${trabajador.hora_inicio}</td>
                        <td>${trabajador.hora_fin}</td>
                    </tr>`;
                });
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-horario-trabajador').innerHTML = tabla;
            } else {
                alert('Error al obtener los horarios de los trabajadores');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los horarios de los trabajadores');
        });
    }
}

function obtenerTrabajadoresSelect() {
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
                let trabajadores = data.data;
                const selectTrabajadores = document.getElementById('trabajador');
                selectTrabajadores.innerHTML = ''; // Limpiar el contenido del select

                //agregar una opción por defecto seleccionada y deshabilitada
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Selecciona un trabajador';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                selectTrabajadores.appendChild(defaultOption);
                trabajadores.forEach(trabajador => {
                    const option = document.createElement('option');
                    option.value = trabajador.id_usuario;
                    option.textContent = `${trabajador.nombre} ${trabajador.paterno} ${trabajador.materno}`;
                    selectTrabajadores.appendChild(option);
                });
            } else {
                alert('Error al obtener los trabajadores');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los trabajadores');
        });
    }
}

function obtenerHorarioDiasSelect() {
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-horario-dias/";
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
                let dias = data.data;
                const selectDias = document.getElementById('diasHorario');
                selectDias.innerHTML = ''; // Limpiar el contenido del select

                //agregar una opción por defecto seleccionada y deshabilitada
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Selecciona un día';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                selectDias.appendChild(defaultOption);
                dias.forEach(dia => {
                    const option = document.createElement('option');
                    option.value = dia.id_cat_horario_dia;
                    option.textContent = dia.dias;
                    selectDias.appendChild(option);
                });
            } else {
                alert('Error al obtener los días del horario');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener los días del horario');
        });
    }
}

function obtenerHorarioHorasSelect() {
    const token = obetenerToken();
    const url = "http://127.0.0.1:8000/usuario/obtener-horario-horas/";
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
                let horas = data.data;
                const selectHoras = document.getElementById('horasHorario');
                selectHoras.innerHTML = ''; // Limpiar el contenido del select

                //agregar una opción por defecto seleccionada y deshabilitada
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Selecciona una hora';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                selectHoras.appendChild(defaultOption);
                horas.forEach(hora => {
                    const option = document.createElement('option');
                    option.value = hora.id_cat_horarios_hora;
                    option.textContent = `${hora.hora_entrada} - ${hora.hora_salida}`;
                    selectHoras.appendChild(option);
                });
            } else {
                alert('Error al obtener las horas del horario');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener las horas del horario');
        });
    }
}

function registrar(formSerialize, url, idModal) {
    const token = obetenerToken();
    const completeUrl = `http://127.0.0.1:8000/${url}`;
    if (token) {
        fetch(completeUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token,
                ...formSerialize
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.estatus === 200) {
                alert('Registro exitoso');
                generarTablaHorarioDias();
                generarTablaHorarioHoras();
                generarTablaHorarioTrabajador();
                obtenerTrabajadoresSelect();
                obtenerHorarioDiasSelect();
                obtenerHorarioHorasSelect();
                // Cerrar el modal usando el atributo data-bs-dismiss="modal"
                const modal = document.getElementById(idModal);
                if (modal) {
                    const closeBtn = modal.querySelector('[data-bs-dismiss="modal"]');
                    if (closeBtn) {
                        closeBtn.click();
                    }
                }
            } else {
                alert('Error al registrar: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    } else {
        console.error('Token no encontrado en las cookies');
    }
}

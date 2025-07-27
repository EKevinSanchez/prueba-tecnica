let catalogoProductos = [];
function generarTablaProductos(){
    let url = "http://127.0.0.1:8000/producto/obtener-productos/"
    const token = obetenerToken();

    if (token) {
        //consultar mediante fetch
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.estatus === 200) {
                let productos = data.data;
                console.log(productos);
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre</th><th>Tipo de Producto</th><th>Inventario</th></tr></thead><tbody>';
                
                productos.forEach(producto => {
                    tabla += `<tr>
                        <td>${producto.id_producto}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.fk_id_cat_producto__nombre}</td>
                        <td>${producto.inventario}</td>
                    </tr>`;
                });
                
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-prodcutos').innerHTML = tabla;
            } else {
                console.error('Error al obtener los productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    } else {
        console.error('Token no encontrado en las cookies');
    }
}
function generarTablaProductosEntrada(){
    let url = "http://127.0.0.1:8000/producto/obtener-productos/"
    const token = obetenerToken();

    if (token) {
        //consultar mediante fetch
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.estatus === 200) {
                let productos = data.data;
                console.log(productos);
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre</th><th>Tipo de Producto</th><th>Precio</th><th>Inventario</th><th>Codigo</th></tr></thead><tbody>';
                
                productos.forEach(producto => {
                    tabla += `<tr>
                        <td>${producto.id_producto}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.fk_id_cat_producto__nombre}</td>
                        <td>$${producto.precio}</td>
                        <td>${producto.inventario}</td>
                        <td>${producto.sku}</td>
                    </tr>`;
                });
                
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-prodcutos').innerHTML = tabla;
            } else {
                console.error('Error al obtener los productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    } else {
        console.error('Token no encontrado en las cookies');
    }
}

function generarTablaTipoProductos(){
    let url = "http://127.0.0.1:8000/producto/obtener-cat-productos/"
    const token = obetenerToken();
    if (token) {
        //consultar mediante fetch
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'access_token': token
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.estatus === 200) {
                let categorias = data.data;
                let tabla = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre</th><th>Descripción</th></tr></thead><tbody>';
                
                categorias.forEach(categoria => {
                    tabla += `<tr>
                        <td>${categoria.id_cat_producto}</td>
                        <td>${categoria.nombre}</td>
                        <td>${categoria.descripcion}</td>
                    </tr>`;
                });
                
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-tipo-productos').innerHTML = tabla;
            } else {
                console.error('Error al obtener las categorías de productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    } else {
        console.error('Token no encontrado en las cookies');
    }
}

function generarTablaProductosVenta() {
    const url = "http://127.0.0.1:8000/producto/obtener-ventas/"
    const token = obetenerToken();
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
                let ventas = data.data;
                let tabla = '<table class="table table-striped"><thead><tr><th>ID Venta</th><th>Fecha</th><th>Total</th></tr></thead><tbody>';
                ventas.forEach(venta => {
                    tabla += `<tr>
                        <td>${venta.id_venta}</td>
                        <td>${new Date(venta.fecha_venta).toLocaleDateString()}</td>
                        <td>$${venta.total}</td>
                    </tr>`;
                });
                tabla += '</tbody></table>';
                document.getElementById('div-tabla-ventas').innerHTML = tabla;

            } else {
                console.error('Error al obtener los productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    }
    else {
        console.error('Token no encontrado en las cookies');
    }
}

function obetenerToken() {
    const cookies = document.cookie.split(';');
    const tokenCookie = cookies.find(cookie => cookie.trim().startsWith('token='));
    if (tokenCookie) {
        return decodeURIComponent(tokenCookie.split('=')[1]);
    }
    return null;
}

function registrar(formSerialize, url, entrada= false) {
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
                generarTablaProductos();
                if (entrada) {
                    generarTablaProductosEntrada();
                }else{
                    generarTablaTipoProductos();
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

function obtenerTiposProductos() {
    let url = "http://127.0.0.1:8000/producto/obtener-cat-productos/";
    const token = obetenerToken();
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
                let tiposProductos = data.data;
                let select = document.getElementById('tipoProducto');
                select.innerHTML = ''; // Limpiar opciones existentes
                tiposProductos.forEach(tipo => {
                    let option = document.createElement('option');
                    option.value = tipo.id_cat_producto;
                    option.textContent = tipo.nombre;
                    select.appendChild(option);
                });
            } else {
                console.error('Error al obtener los tipos de productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    } else {
        console.error('Token no encontrado en las cookies');
    }
}

function obtenerProductos(){
    let url = "http://127.0.0.1:8000/producto/obtener-productos/";
    const token = obetenerToken();
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
                let productos = data.data;
                let select = document.getElementById('productoEntrada');
                select.innerHTML = ''; // Limpiar opciones existentes
                // Agregar una opción por defecto que este seleccionada y este desactivada
                let defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Seleccione un producto';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                select.appendChild(defaultOption);
                // Llenar el select con los productos obtenidos
                productos.forEach(producto => {
                    catalogoProductos.push(producto);
                    let option = document.createElement('option');
                    option.value = producto.id_producto;
                    option.textContent = `${producto.nombre} - ${producto.sku}`;
                    select.appendChild(option);
                });
            } else {
                console.error('Error al obtener los productos:', data.message);
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
    }
    else {
        console.error('Token no encontrado en las cookies');
    }
}

function agregarProductoVenta() {
    const productoId = document.getElementById('productoEntrada').value;
    const cantidad = document.getElementById('cantidadProducto').value;

    if (productoId && cantidad) {
        const producto = catalogoProductos.find(p => p.id_producto == productoId);
        if(cantidad > producto.inventario) {
            alert('Cantidad no disponible en inventario');
            return;
        }
        if (producto) {
            const total = producto.precio * cantidad;
            const fila = `<tr>
                <td>${producto.nombre}</td>
                <td>${cantidad}</td>
                <td>$${producto.precio}</td>
                <td>$${total}</td>
            </tr>`;
            document.getElementById('tablaProductosVenta').insertAdjacentHTML('beforeend', fila);
            // Limpiar los campos después de agregar el producto
            document.getElementById('productoEntrada').value = '';
            document.getElementById('cantidadProducto').value = '';
            //agregar el producto al input oculto para enviar al servidor
            const inputProductos = document.getElementById('productosVenta');
            const productosActuales = inputProductos.value ? JSON.parse(inputProductos.value) : [];
            productosActuales.push({
                id_producto: producto.id_producto,
                cantidad: cantidad,
                precio: producto.precio,
                total: total
            });
            inputProductos.value = JSON.stringify(productosActuales);
        }
    } else {
        alert('Por favor, seleccione un producto y una cantidad.');
    }
}

function registrarVenta() {
    const productosVenta = document.getElementById('productosVenta').value;
    if (productosVenta) {
        const url = "http://127.0.0.1:8000/producto/registrar-venta/"
        const token = obetenerToken();
        if (token) {
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'access_token': token,
                    'productos': JSON.parse(productosVenta)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.estatus === 200) {
                    alert('Venta registrada exitosamente');
                    // Limpiar la tabla y el input oculto
                    document.getElementById('tablaProductosVenta').innerHTML = '';
                    document.getElementById('productosVenta').value = '';
                    //Cerrar el modal
                    $('#modalRegistrarVenta').modal('hide');
                    generarTablaProductosVenta();

                } else {
                    alert('Error al registrar la venta: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
        }
        else {
            console.error('Token no encontrado en las cookies');
        }
    } else {
        alert('No hay productos en la venta para registrar.');
    }
}
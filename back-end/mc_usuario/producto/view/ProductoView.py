import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework_simplejwt.tokens import AccessToken

from producto.models import CatProducto, EntradaInventario, Producto, Venta, DetalleVenta
from usuario.models import Usuario


@csrf_exempt
def registrar_producto(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            fk_id_cat_producto = data.get('fk_id_cat_producto', '').strip()
            nombre = data.get('nombre', '').strip()
            inventario = data.get('inventario', '').strip()
            precio = data.get('precio', '').strip()
            sku = data.get('sku', '').strip()


            if not nombre or not inventario or not precio or not fk_id_cat_producto or not sku:
                return JsonResponse({'message': 'Todos los campos son requeridos.', 'estatus': 400, 'data': []}, status=400)

            # Verificar que fk_id_cat_producto sea un entero válido, se convierta a int y ver si existe en la base de datos
            try:
                fk_id_cat_producto = int(fk_id_cat_producto)
            except ValueError:
                return JsonResponse({'message': 'El campo fk_id_cat_producto debe ser un número entero.', 'estatus': 400, 'data': []}, status=400)

            cat_producto = CatProducto.objects.filter(id_cat_producto=fk_id_cat_producto).first()
            if not cat_producto:
                return JsonResponse({'message': 'Categoría de producto no encontrada.', 'estatus': 404, 'data': []}, status=404)
            # Verificar si el SKU ya existe
            if Producto.objects.filter(sku=sku).exists():
                return JsonResponse({'message': 'El SKU ya existe.', 'estatus': 400, 'data': []}, status=400)
            # Crear el nuevo producto
            with transaction.atomic():
                nuevo_producto = Producto(
                    fk_id_cat_producto_id=fk_id_cat_producto,
                    nombre=nombre,
                    inventario=int(inventario),
                    precio=float(precio),
                    sku=sku
                )
                nuevo_producto.save()
            # Retornar respuesta exitosa
            return JsonResponse({'message': 'Producto registrado exitosamente.', 'estatus': 200, 'data': []}, status=200)


            return JsonResponse({'message': 'Producto agregado exitosamente.', 'estatus': 200, 'data': []}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return JsonResponse({'message': 'Error al agregar producto.', 'estatus': 500, 'data': []}, status=500)

@csrf_exempt
def registrar_cat_producto(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()

            if not nombre:
                return JsonResponse({'message': 'El campo nombre es requerido.', 'estatus': 400, 'data': []}, status=400)

            # Verificar si la categoría ya existe
            if CatProducto.objects.filter(nombre=nombre).exists():
                return JsonResponse({'message': 'La categoría de producto ya existe.', 'estatus': 400, 'data': []}, status=400)

            # Crear la nueva categoría
            with transaction.atomic():
                nueva_categoria = CatProducto(
                    nombre=nombre,
                    descripcion=descripcion
                )
                nueva_categoria.save()

            return JsonResponse({'message': 'Categoría de producto registrada exitosamente.', 'estatus': 200, 'data': []}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al registrar categoría de producto: {e}")
        return JsonResponse({'message': 'Error al registrar categoría de producto.', 'estatus': 500, 'data': []}, status=500)

@csrf_exempt
def registrar_entrada_inventario(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            fk_id_producto = data.get('fk_id_producto', '').strip()
            cantidad = data.get('cantidad', '').strip()

            if not fk_id_producto or not cantidad:
                return JsonResponse({'message': 'Todos los campos son requeridos.', 'estatus': 400, 'data': []}, status=400)

            # Verificar que fk_id_producto sea un entero válido
            try:
                fk_id_producto = int(fk_id_producto)
            except ValueError:
                return JsonResponse({'message': 'El campo fk_id_producto debe ser un número entero.', 'estatus': 400, 'data': []}, status=400)

            producto = Producto.objects.filter(id_producto=fk_id_producto).first()
            if not producto:
                return JsonResponse({'message': 'Producto no encontrado.', 'estatus': 404, 'data': []}, status=404)

            # Crear la entrada de inventario
            with transaction.atomic():
                # Actualizar el inventario del producto
                producto.inventario += int(cantidad)
                producto.save()
                # Registrar el producto actualizado
                entrada_inventario = EntradaInventario(
                    fk_id_producto_id=fk_id_producto,
                    cantidad=int(cantidad)
                )
                entrada_inventario.save()

            return JsonResponse({'message': 'Entrada de inventario registrada exitosamente.', 'estatus': 200, 'data': []}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al registrar entrada de inventario: {e}")
        return JsonResponse({'message': 'Error al registrar entrada de inventario.', 'estatus': 500, 'data': []}, status=500)

@csrf_exempt
def registrar_venta(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            usuario = autenticar_usuario(data.get('access_token', ''))
            productos_venta = data.get('productos', [])

            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)

            # Recorrer los productos y validar
            if not productos_venta:
                return JsonResponse({'message': 'Se deben proporcionar productos para la venta.', 'estatus': 400, 'data': []}, status=400)
            total_venta = 0
            usuarioRegistro = Usuario.objects.filter(id_usuario=usuario['user']['id_usuario']).first()
            with transaction.atomic():
                venta_actual = Venta(
                    fk_id_usuario=usuarioRegistro,
                    total=total_venta
                )
                venta_actual.save()
                for item in productos_venta:
                    fk_id_producto = item.get('id_producto', 0)
                    cantidad = int(item.get('cantidad', 0))

                    if not fk_id_producto or not cantidad:
                        return JsonResponse({'message': 'Todos los campos son requeridos.', 'estatus': 400, 'data': []}, status=400)

                    # Verificar que fk_id_producto sea un entero válido
                    try:
                        fk_id_producto = int(fk_id_producto)
                        cantidad = int(cantidad)
                    except ValueError:
                        return JsonResponse({'message': 'Los campos fk_id_producto y cantidad deben ser números enteros.', 'estatus': 400, 'data': []}, status=400)

                    producto = Producto.objects.filter(id_producto=fk_id_producto).first()
                    if not producto:
                        return JsonResponse({'message': f'Producto con ID {fk_id_producto} no encontrado.', 'estatus': 404, 'data': []}, status=404)

                    if producto.inventario < cantidad:
                        return JsonResponse({'message': f'Inventario insuficiente para el producto {producto.nombre}.', 'estatus': 400, 'data': []}, status=400)

                    # Actualizar inventario del producto
                    producto.inventario -= cantidad
                    producto.save()

                    subtotal = producto.precio * cantidad

                    # Registrar el detalle de la venta
                    detalle_venta = DetalleVenta(
                        fk_id_producto_id=fk_id_producto,
                        fk_id_venta=venta_actual,
                        cantidad=cantidad,
                        subtotal=subtotal
                    )
                    detalle_venta.save()

                    # Calcular total de la venta
                    total_venta += producto.precio * cantidad
                # Guardar la venta
                venta_actual.total = total_venta
                venta_actual.save()

            return JsonResponse({'message': 'Venta registrada exitosamente.', 'estatus': 200, 'data': []}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al registrar venta: {e}")
        return JsonResponse({'message': 'Error al registrar venta.', 'estatus': 500, 'data': []}, status=500)

def autenticar_usuario(access_token):
    response = {
        'status': True,
        'user': {
            'id_usuario': None,
            'email': None,
            'nombre': None,
            'paterno': None,
            'materno': None,
            'telefono': None
        },
        'message': ''
    }
    if not access_token:
        response['status'] = False
        response['message'] = 'Token de acceso no proporcionado.'
        return response
    try:
        usuario = AccessToken(access_token)
        id_usuario = usuario['user_id']
        usuario_obj = Usuario.objects.get(id_usuario=id_usuario)
        response['user'] = {
            'id_usuario': usuario_obj.id_usuario,
            'email': usuario_obj.email,
            'nombre': usuario_obj.nombre,
            'paterno': usuario_obj.paterno,
            'materno': usuario_obj.materno,
            'telefono': usuario_obj.telefono
        }
        response['message'] = 'Usuario autenticado exitosamente.'
        return response
    except Exception as e:
        print(f"Error validating token: {e}")
        response['status'] = False
        response['message'] = 'Token de acceso inválido o usuario no encontrado.'
        return response

@csrf_exempt
def obtener_productos(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)
            # Obtener todos los productos
            productos = Producto.objects.all().values(
                'id_producto', 'fk_id_cat_producto__nombre', 'nombre', 'inventario', 'precio', 'estatus', 'sku'
            ).filter(
                estatus=True
            ).order_by('nombre')
            return JsonResponse({'message': 'Productos obtenidos exitosamente.', 'estatus': 200, 'data': list(productos)}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return JsonResponse({'message': 'Error al obtener productos.', 'estatus': 500, 'data': []}, status=500)

@csrf_exempt
def obtener_ventas(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)

            # Obtener todas las ventas del usuario autenticado
            ventas = Venta.objects.filter(fk_id_usuario=usuario['user']['id_usuario']).values(
                'id_venta', 'fecha_venta', 'total'
            ).order_by('-fecha_venta')

            return JsonResponse({'message': 'Ventas obtenidas exitosamente.', 'estatus': 200, 'data': list(ventas)}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        return JsonResponse({'message': 'Error al obtener ventas.', 'estatus': 500, 'data': []}, status=500)

@csrf_exempt
def obtener_cat_productos(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)

            # Obtener todas las categorías de productos
            categorias = CatProducto.objects.all().values(
                'id_cat_producto', 'nombre', 'descripcion'
            ).filter(
                estatus=True
            )

            return JsonResponse({'message': 'Categorías de productos obtenidas exitosamente.', 'estatus': 200, 'data': list(categorias)}, status=200)
        else:
            return JsonResponse({'message': 'Método no permitido.', 'estatus': 405, 'data': []}, status=405)
    except Exception as e:
        print(f"Error al obtener categorías de productos: {e}")
        return JsonResponse({'message': 'Error al obtener categorías de productos.', 'estatus': 500, 'data': []}, status=500)

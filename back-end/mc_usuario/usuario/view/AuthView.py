import random
import string
import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from usuario.models import Usuario, CatTipoUsuario, CatHorarioHora, CatHorarioDia, HorarioTrabajador


@csrf_exempt
def auth_login(request):
    if request.method == 'POST':
        try:
            #parsear el request.body a json
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            email = data.get('email', '').strip()
            upass = data.get('upass', '').strip()


            if not email or not upass:
                return JsonResponse({'message': 'Los campos de contraseña y email son requeridos.', 'estatus':400, 'data':[]}, status=400)

            usuario = Usuario.objects.get(email=email)
            if usuario.estatus == False:
                return JsonResponse({'message': 'Usuario inactivo.', 'estatus':400, 'data':[]}, status=400)

            if not usuario.check_upass(upass):
                return JsonResponse({'message': 'Contraseña incorrecta.', 'estatus':400, 'data':[]}, status=400)

            login(request, usuario)
            refresh = RefreshToken.for_user(usuario)
            access_token = str(refresh.access_token)
            usuario.access_token = access_token  # Guardar el token en el usuario
            usuario.save()  # Guardar el usuario con el nuevo token

            return JsonResponse({
                'message': 'Login exitoso',
                'estatus': 200,
                'data': {
                    'id_usuario': usuario.id_usuario,
                    'email': usuario.email,
                    'nombre': usuario.nombre,
                    'paterno': usuario.paterno,
                    'materno': usuario.materno,
                    'telefono': usuario.telefono,
                    'tipo_usuario': usuario.fk_id_cat_tipo_usuario.id_cat_tipo_usuario,
                    'nombre_tipo_usuario': usuario.fk_id_cat_tipo_usuario.nombre,
                    'access_token': access_token
                }
            }, status=200)

        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({'message': 'Login failed'}, status=400)

@csrf_exempt
def agregar_usuario(request):
    try:
        if request.method == 'POST':
            print(request.POST)  # Para depuración
            if((request.POST['email']).strip() == (request.POST['email_validado']).strip()):

                upass_plano = generar_contraseña(8)
                print(f"Contraseña generada: {upass_plano}")  # Para depuración
                upass = make_password(upass_plano)
                with transaction.atomic():
                    nuevo_usuario = Usuario(
                        fk_id_cat_tipo_usuario_id=request.POST['fk_id_cat_tipo_usuario'],
                        email=request.POST['email'].strip(),
                        upass=upass,
                        nombre=request.POST['nombre'].strip(),
                        paterno=request.POST['paterno'].strip(),
                        materno=request.POST['materno'].strip(),
                        telefono=request.POST['telefono'].strip()
                    )
                    nuevo_usuario.save()
                return JsonResponse({
                    'message': 'Usuario agregado exitosamente',
                    'estatus': 200,
                    'data': {
                        'id_usuario': nuevo_usuario.id_usuario,
                        'email': nuevo_usuario.email,
                        'nombre': nuevo_usuario.nombre,
                        'paterno': nuevo_usuario.paterno,
                        'materno': nuevo_usuario.materno,
                        'telefono': nuevo_usuario.telefono,
                        'contraseña_plana': upass_plano
                    }
                }, status=200)
    except Exception as e:
        print(f"Error during agregar_usuario: {e}")
        return JsonResponse({'message': 'Error al agregar usuario'}, status=400)

def generar_contraseña(longitud=8):
    caracteres = string.ascii_letters  # Incluye tanto mayúsculas como minúsculas
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

@csrf_exempt
def agregar_tipo_usuario(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            if not request.POST.get('nombre'):
                return JsonResponse({'message': 'El campo nombre es requerido.', 'estatus': 400, 'data': []}, status=400)
            with transaction.atomic():
                nuevo_tipo_usuario = CatTipoUsuario(
                    nombre=request.POST['nombre'].strip(),
                    descripcion=request.POST.get('descripcion', '').strip()
                )
                nuevo_tipo_usuario.save()
            return JsonResponse({
                'message': 'Tipo de usuario agregado exitosamente',
                'estatus': 200,
                'data': {
                    'id_cat_tipo_usuario': nuevo_tipo_usuario.id_cat_tipo_usuario,
                    'nombre': nuevo_tipo_usuario.nombre,
                }
            }, status=200)
    except Exception as e:
        print(f"Error during agregar_tipo_trabajador: {e}")
        return JsonResponse({'message': 'Error al agregar tipo de trabajador'}, status=400)

@csrf_exempt
def agregrar_horario_hora(request): 
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            hora_entrada = data.get('hora_entrada', '').strip()
            hora_salida = data.get('hora_salida', '').strip()
            if not access_token:
                return JsonResponse({'message': 'El token de acceso es requerido.', 'estatus': 400, 'data': []},
                                    status=400)

            if not hora_entrada or not hora_salida:
                return JsonResponse({'message': 'Los campos hora_entrada y hora_salida son requeridos.', 'estatus': 400, 'data': []}, status=400)

            try:
                usuario = AccessToken(access_token)
                id_usuario = usuario['user_id']
                usuario_obj = Usuario.objects.get(id_usuario=id_usuario)
            except Exception as e:
                print(f"Error validating token: {e}")
                return JsonResponse({'message': 'Token inválido o expirado.', 'estatus': 401, 'data': []}, status=401)
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse(
                    {'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []},
                    status=403)
            with transaction.atomic():
                nuevo_horario_hora = CatHorarioHora(
                    hora_entrada=hora_entrada,
                    hora_salida=hora_salida,
                )
                nuevo_horario_hora.save()
            return JsonResponse({
                'message': 'Horario hora agregado exitosamente',
                'estatus': 200,
                'data': {
                    'id_cat_horarios_hora': nuevo_horario_hora.id_cat_horarios_hora,
                    'hora_entrada': nuevo_horario_hora.hora_entrada,
                    'hora_salida': nuevo_horario_hora.hora_salida,
                }
            }, status=200)
    except Exception as e:
        print(f"Error during agregar_tipo_trabajador: {e}")
        return JsonResponse({'message': 'Error al agregar horas del horario'}, status=400)

@csrf_exempt
def agregar_horario_dias(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            dias = data.get('dias', '').strip()
            if not access_token:
                return JsonResponse({'message': 'El token de acceso es requerido.', 'estatus': 400, 'data': []}, status=400)
            if not dias:
                return JsonResponse({'message': 'El campo dias es requerido.', 'estatus': 400, 'data': []}, status=400)

            try:
                usuario = AccessToken(access_token)
                id_usuario = usuario['user_id']
                usuario_obj = Usuario.objects.get(id_usuario=id_usuario)
            except Exception as e:
                print(f"Error validating token: {e}")
                return JsonResponse({'message': 'Token inválido o expirado.', 'estatus': 401, 'data': []}, status=401)
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)

            with transaction.atomic():
                nuevo_horario_dia = CatHorarioDia(
                    dias=dias,
                )
                nuevo_horario_dia.save()
            return JsonResponse({
                'message': 'Horario día agregado exitosamente',
                'estatus': 200,
                'data': {
                    'id_cat_horarios_dia': nuevo_horario_dia.id_cat_horario_dia,
                    'dias': nuevo_horario_dia.dias,
                }
            }, status=200)
    except Exception as e:
        print(f"Error during agregar_tipo_trabajador: {e}")
        return JsonResponse({'message': 'Error al agregar días del horario'}, status=400)

@csrf_exempt
def agregar_horario_trabajador(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario_trabajador = data.get('usuario_trabajador', '').strip()
            id_cat_horario_dia = data.get('fk_id_cat_horario_dia', '').strip()
            id_cat_horario_hora = data.get('fk_id_cat_horario_hora', '').strip()

            try:
                usuario = AccessToken(access_token)
                id_usuario = usuario['user_id']
                usuario_obj = Usuario.objects.get(id_usuario=id_usuario)
            except Exception as e:
                print(f"Error validating token: {e}")
                return JsonResponse({'message': 'Token inválido o expirado.', 'estatus': 401, 'data': []}, status=401)
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)

            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)

            if not usuario_trabajador or not id_cat_horario_dia or not id_cat_horario_hora:
                return JsonResponse({'message': 'Los campos usuario_trabajador, fk_id_cat_horario_dia y fk_id_cat_horario_hora son requeridos.', 'estatus': 400, 'data': []}, status=400)
            if not access_token:
                return JsonResponse({'message': 'El token de acceso es requerido.', 'estatus': 400, 'data': []}, status=400)

            # Validar que el usuario existe
            try:
                usuario = Usuario.objects.get(id_usuario=usuario_trabajador)
            except Usuario.DoesNotExist:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            # Validar que el día del horario existe
            try:
                horario_dia = CatHorarioDia.objects.get(id_cat_horarios_dia=id_cat_horario_dia)
            except CatHorarioDia.DoesNotExist:
                return JsonResponse({'message': 'Día del horario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            # Validar que la hora del horario existe
            try:
                horario_hora = CatHorarioHora.objects.get(id_cat_horarios_hora=id_cat_horario_hora)
            except CatHorarioHora.DoesNotExist:
                return JsonResponse({'message': 'Hora del horario no encontrada.', 'estatus': 404, 'data': []}, status=404)

            with transaction.atomic():
                nuevo_horario_trabajador = HorarioTrabajador(
                    fk_id_usuario=usuario,
                    fk_id_cat_horario_dia=horario_dia,
                    fk_id_cat_horario_hora=horario_hora
                )
                nuevo_horario_trabajador.save()
            return JsonResponse({
                'message': 'Horario trabajador agregado exitosamente',
                'estatus': 200,
                'data': {
                    'id_horario_trabajador': nuevo_horario_trabajador.id_horario_trabajador,
                    'fk_id_usuario': nuevo_horario_trabajador.fk_id_usuario.id_usuario,
                    'fk_id_cat_horario_dia': nuevo_horario_trabajador.fk_id_cat_horario_dia.id_cat_horario_dia,
                    'fk_id_cat_horario_hora': nuevo_horario_trabajador.fk_id_cat_horario_hora.id_cat_horarios_hora,
                }
            }, status=200)
    except Exception as e:
        print(f"Error during agregar_horario_trabajador: {e}")
        return JsonResponse({'message': 'Error al agregar horario del trabajador'}, status=400)

@csrf_exempt
def obtener_tipos_usuario(request):
    try:
        if request.method == 'POST':
            #Validar el token enviado en la peticion
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            if not access_token:
                return JsonResponse({'message': 'El token de acceso es requerido.', 'estatus': 400, 'data': []}, status=400)
            try:
                usuario = AccessToken(access_token)
                id_usuario = usuario['user_id']
                usuario_obj = Usuario.objects.get(id_usuario=id_usuario)
            except Exception as e:
                print(f"Error validating token: {e}")
                return JsonResponse({'message': 'Token inválido o expirado.', 'estatus': 401, 'data': []}, status=401)
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario == 1:
                tipos_usuario = CatTipoUsuario.objects.all().values(
                    'id_cat_tipo_usuario', 'nombre'
                )
                return JsonResponse({
                    'message': 'Tipos de usuario obtenidos exitosamente',
                    'estatus': 200,
                    'data': list(tipos_usuario)
                }, status=200)
            else:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)
    except Exception as e:
        print(f"Error during obtener_tipo_usuario: {e}")
        return JsonResponse({'message': 'Error al obtener tipos de usuario'}, status=400)

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
def obtener_usuarios(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)
            if usuario['user']['id_usuario'] is None:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)

            usuario_obj = Usuario.objects.get(id_usuario=usuario['user']['id_usuario'])
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario == 1:
                usuarios = Usuario.objects.all().values(
                    'id_usuario', 'email', 'nombre', 'paterno', 'materno', 'telefono', 'fk_id_cat_tipo_usuario__id_cat_tipo_usuario', 'fk_id_cat_tipo_usuario__nombre', 'estatus'
                ).filter(
                    estatus=True
                )
                return JsonResponse({
                    'message': 'Usuarios obtenidos exitosamente',
                    'estatus': 200,
                    'data': list(usuarios)
                }, status=200)
            else:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)
    except Exception as e:
        print(f"Error during obtener_usuarios: {e}")
        return JsonResponse({'message': 'Error al obtener usuarios'}, status=400)


@csrf_exempt
def obtener_horario_dias(requestt):
    try:
        if requestt.method == 'POST':
            json_body = requestt.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)
            if usuario['user']['id_usuario'] is None:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)

            usuario_obj = Usuario.objects.get(id_usuario=usuario['user']['id_usuario'])
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)
            horario_dias = CatHorarioDia.objects.all().values(
                'id_cat_horario_dia', 'dias'
            ).filter(
                estatus=True
            )
            return JsonResponse({
                'message': 'Días del horario obtenidos exitosamente',
                'estatus': 200,
                'data': list(horario_dias)
            }, status=200)
    except Exception as e:
        print(f"Error during obtener_horario_dias: {e}")
        return JsonResponse({'message': 'Error al obtener días del horario'}, status=400)

@csrf_exempt
def obtener_horario_horas(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)
            if usuario['user']['id_usuario'] is None:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)

            usuario_obj = Usuario.objects.get(id_usuario=usuario['user']['id_usuario'])
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)
            horario_horas = CatHorarioHora.objects.all().values(
                'id_cat_horarios_hora', 'hora_entrada', 'hora_salida'
            ).filter(
                estatus=True
            )
            return JsonResponse({
                'message': 'Horas del horario obtenidas exitosamente',
                'estatus': 200,
                'data': list(horario_horas)
            }, status=200)
    except Exception as e:
        print(f"Error during obtener_horario_horas: {e}")
        return JsonResponse({'message': 'Error al obtener horas del horario'}, status=400)

@csrf_exempt
def obtener_horario_trabajador(request):
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            data = json.loads(json_body)
            access_token = data.get('access_token', '').strip()
            usuario = autenticar_usuario(access_token)
            if not usuario['status']:
                return JsonResponse({'message': usuario['message'], 'estatus': 401, 'data': []}, status=401)
            if usuario['user']['id_usuario'] is None:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)

            usuario_obj = Usuario.objects.get(id_usuario=usuario['user']['id_usuario'])
            if not usuario_obj:
                return JsonResponse({'message': 'Usuario no encontrado.', 'estatus': 404, 'data': []}, status=404)
            if usuario_obj.fk_id_cat_tipo_usuario.id_cat_tipo_usuario != 1:
                return JsonResponse({'message': 'No tienes permisos para realizar esta acción.', 'estatus': 403, 'data': []}, status=403)

            horario_trabajadores = HorarioTrabajador.objects.all().values(
                'id_horario_trabajador',
                'fk_id_usuario__id_usuario',
                'fk_id_usuario__nombre',
                'fk_id_cat_horario_dia__dias',
                'fk_id_cat_horario_hora__hora_entrada',
                'fk_id_cat_horario_hora__hora_salida'
            ).filter(
                fk_id_usuario__estatus=True
            )
            return JsonResponse({
                'message': 'Horarios de trabajadores obtenidos exitosamente',
                'estatus': 200,
                'data': list(horario_trabajadores)
            }, status=200)
    except Exception as e:
        print(f"Error during obtener_horario_trabajador: {e}")
        return JsonResponse({'message': 'Error al obtener horarios de trabajadores'}, status=400)
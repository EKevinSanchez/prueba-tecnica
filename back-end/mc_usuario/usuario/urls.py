from django.urls import path

from usuario.view.AuthView import auth_login, agregar_usuario, obtener_tipos_usuario, obtener_usuarios, \
    obtener_horario_dias, obtener_horario_horas, obtener_horario_trabajador, agregar_horario_dias, agregrar_horario_hora

urlpatterns = [
    path('login/', auth_login, name='auth_login'),
    path('agregar_usuario/', agregar_usuario, name='agregar_usuario'),
    path('obtener-tipos-usuario/', obtener_tipos_usuario, name='obtener_tipos_usuario'),
    path('obtener-usuarios/', obtener_usuarios, name= 'obtener_usuarios'),
    path('obtener-horario-dias/', obtener_horario_dias, name='obtener_horario_dias'),
    path('obtener-horario-horas/', obtener_horario_horas, name='obtener_horario_horas'),
    path('obtener-horario-trabajador/', obtener_horario_trabajador, name='obtener_horario_trabajador'),
    path('agregar-horario-dias/', agregar_horario_dias, name='agregar_horario_dias'),
    path('agregar-horario-horas/', agregrar_horario_hora, name='agregar_horario_hora'),

]
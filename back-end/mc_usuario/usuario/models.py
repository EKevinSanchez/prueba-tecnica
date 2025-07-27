from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.

class CatTipoUsuario(models.Model):
    id_cat_tipo_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50,
        unique=True,
        db_column='nombre'
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'cat_tipo_usuario'
        verbose_name = 'Categoría de Tipo de Usuario'
        verbose_name_plural = 'Categorías de Tipos de Usuario'
        ordering = ['nombre']


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    fk_id_cat_tipo_usuario = models.ForeignKey(
        CatTipoUsuario,
        on_delete=models.CASCADE,
        db_column='fk_id_cat_tipo_usuario'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_column='email'
    )
    upass = models.CharField(
        max_length=254,
        db_column='upass'
    )
    nombre = models.CharField(
        max_length=100,
        db_column='nombre'
    )
    paterno = models.CharField(
        max_length=100,
        db_column='paterno'
    )
    materno = models.CharField(
        max_length=100,
        db_column='materno'
    )
    telefono = models.CharField(
        max_length=15,
        db_column='telefono',
        null=True,
        blank=True
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_column='updated_at'
    )
    last_login = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.nombre} {self.paterno} {self.materno} ({self.email})"

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['paterno', 'materno', 'nombre']

    def set_upass(self, upass):
        """Generar la contraseña encriptada."""
        self.upass = make_password(upass)

    def check_upass(self, upass):
        """Verificar la contraseña ingresada."""
        return check_password(upass, self.upass)

class CatHorarioDia(models.Model):
    id_cat_horario_dia = models.AutoField(primary_key=True)
    dias = models.CharField(
        max_length=20,
        unique=True,
        db_column='dias'
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )

    def __str__(self):
        return self.dias

    class Meta:
        db_table = 'cat_horarios_dias'
        verbose_name = 'Categoría de Horario por Día'
        verbose_name_plural = 'Categorías de Horarios por Día'
        ordering = ['dias']

class CatHorarioHora(models.Model):
    id_cat_horarios_hora = models.AutoField(primary_key=True)
    hora_entrada = models.TimeField(
        db_column='hora_entrada'
    )
    hora_salida = models.TimeField(
        db_column='hora_salida'
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )

    def __str__(self):
        return f"{self.hora_entrada} - {self.hora_salida}"

    class Meta:
        db_table = 'cat_horarios_horas'
        verbose_name = 'Categoría de Horario por Hora'
        verbose_name_plural = 'Categorías de Horarios por Hora'
        ordering = ['hora_entrada']

class HorarioTrabajador(models.Model):
    id_horario_trabajador = models.AutoField(primary_key=True)
    fk_id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='fk_id_usuario'
    )
    fk_id_cat_horario_dia = models.ForeignKey(
        CatHorarioDia,
        on_delete=models.CASCADE,
        db_column='fk_id_cat_horario_dia'
    )
    fk_id_cat_horario_hora = models.ForeignKey(
        CatHorarioHora,
        on_delete=models.CASCADE,
        db_column='fk_id_cat_horario_hora'
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )

    class Meta:
        db_table = 'horario_trabajador'
        verbose_name = 'Horario de Trabajador'
        verbose_name_plural = 'Horarios de Trabajadores'
        ordering = ['fk_id_usuario', 'fk_id_cat_horario_dia']
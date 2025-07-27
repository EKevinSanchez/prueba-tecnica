from django.db import models

# Create your models here.

class CatProducto(models.Model):
    id_cat_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=100,
        unique=True,
        db_column='nombre'
    )
    descripcion = models.TextField(
        db_column='descripcion',
        null=True,
        blank=True
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'cat_productos'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'
        ordering = ['nombre']

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    fk_id_cat_producto = models.ForeignKey(
        CatProducto,
        on_delete=models.CASCADE,
        db_column='fk_id_cat_producto'
    )
    nombre = models.CharField(
        max_length=100,
        db_column='nombre'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='precio'
    )
    inventario = models.IntegerField(
        db_column='inventario',
        default=0
    )
    estatus = models.BooleanField(
        default=True,
        db_column='estatus'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        db_column='sku'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

class EntradaInventario(models.Model):
    id_entrada_inventario = models.AutoField(primary_key=True)
    fk_id_producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='fk_id_producto'
    )
    cantidad = models.IntegerField(
        db_column='cantidad'
    )
    fecha_entrada = models.DateTimeField(
        auto_now_add=True,
        db_column='fecha_entrada'
    )

    def __str__(self):
        return f"{self.fk_id_producto.nombre} - {self.cantidad} unidades"
    class Meta:
        db_table = 'entrada_inventario'
        verbose_name = 'Entrada de Inventario'
        verbose_name_plural = 'Entradas de Inventario'
        ordering = ['fecha_entrada']

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fk_id_usuario = models.ForeignKey(
        'usuario.Usuario',
        on_delete=models.CASCADE,
        db_column='fk_id_usuario'
    )
    fecha_venta = models.DateTimeField(
        auto_now_add=True,
        db_column='fecha_venta'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='total'
    )

    def __str__(self):
        return f"Venta #{self.id_venta} - Total: {self.total}"
    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['fecha_venta']

class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    fk_id_producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='fk_id_producto'
    )
    fk_id_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column='fk_id_venta'
    )
    cantidad = models.IntegerField(
        db_column='cantidad'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='subtotal'
    )

    def __str__(self):
        return f"{self.fk_id_producto.nombre} - {self.cantidad} unidades"
    class Meta:
        db_table = 'detalles_ventas'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        ordering = ['fk_id_venta', 'fk_id_producto']
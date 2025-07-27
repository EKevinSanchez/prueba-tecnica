from django.urls import path

from producto.view.ProductoView import obtener_productos, registrar_producto, registrar_cat_producto, \
    registrar_entrada_inventario, registrar_venta, obtener_ventas, obtener_cat_productos

urlpatterns = [
    path('obtener-productos/', obtener_productos, name='obtener_productos'),
    path('registrar-producto/', registrar_producto, name='registrar_producto'),
    path('registrar-cat-producto/', registrar_cat_producto, name='registrar_cat_producto'),
    path('registrar-entrada-inventario/', registrar_entrada_inventario, name= 'registrar_entrada_inventario'),
    path('registrar-venta/', registrar_venta, name='registrar_venta'),
    path('obtener-ventas/', obtener_ventas, name='obtener_ventas'),
    path('obtener-cat-productos/', obtener_cat_productos, name='obtener_cat_productos'),
]
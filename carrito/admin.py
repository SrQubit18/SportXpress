from django.contrib import admin
from .models import *
# Register your models here.

models_list = [Producto,Factura,PedidoEntregado,Venta,VentaProducto]
for element in models_list:
    admin.site.register(element)



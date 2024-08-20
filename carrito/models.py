from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from datetime import datetime

class Factura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=datetime.now)
    products= models.CharField(max_length=10000)
    pendiente = models.BooleanField(default=True)  # True significa pendiente
    entregado = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.numero_factura} - Usuario: {self.usuario.username}"



class PedidoEntregado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrega = models.DateTimeField(auto_now_add=True)    
    
    
    
class Producto(models.Model):
    CATEGORIA_OPCIONES = [
        ('Remeras', 'Remeras'),
        ('Botines', 'Botines'),
        ('Calzado', 'Calzado'),
        ('Pantalones', 'Pantalones'),
        ('Rodilleras', 'Rodilleras'),
        ('Hombreras','Hombreras'),
        ('Coderas','Coderas'),
        ('Cascos','Cascos'),
        ('Chalecos', 'Chalecos'),
        ('Gorras', 'Gorras'),
        ('Guantes', 'Guantes'),
        ('Mochilas', 'Mochilas'),
        ('Toallas', 'Toallas'),
        ('Cinturones', 'Cinturones'),
        ('Bandas elásticas', 'Bandas elásticas'),
        ('Calcetines', 'Calcetines'),
        ('Pantalones cortos', 'Pantalones cortos'),
        ('Pelotas', 'Pelotas'),
        ('Kit entrenamiento', 'Kit entrenamiento'),
        ('otro','otro')
    ]

    MARCA_OPCIONES = [
        ('Nike', 'Nike'),
        ('Adidas', 'Adidas'),
        ('Puma', 'Puma'),
        ('Reebok', 'Reebok'),
        ('Under Armour', 'Under Armour'),
        ('New Balance', 'New Balance'),
        ('Asics', 'Asics'),
        ('Mizuno', 'Mizuno'),
        ('Wilson', 'Wilson'),
        ('Converse', 'Converse'),
        ('Fila', 'Fila'),
        ('Skechers', 'Skechers'),
        ('Champion', 'Champion'),
        ('Saucony', 'Saucony'),
        ('Brooks', 'Brooks'),
        ('Kappa', 'Kappa'),
        ('Vans', 'Vans'),
        ('Lotto', 'Lotto'),
        ('Columbia', 'Columbia'),
        ('Oakley', 'Oakley'),
        ('Hummel', 'Hummel'),
        ('Trekking', 'Trekking'),
        ('Joma', 'Joma'),
        ('Karhu', 'Karhu'),
        ('Hoka One One', 'Hoka One One'),
        ('Palladium', 'Palladium'),
        ('otro','otro')
    ]

    TAMANO_OPCIONES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    GENERO_OPCIONES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Unisex', 'Unisex'),
        ('null', None),
    ]

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    descripcion = models.TextField()
    stock = models.IntegerField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_OPCIONES)
    marca = models.CharField(max_length=50, choices=MARCA_OPCIONES)
    tamaño = models.CharField(max_length=50, choices=TAMANO_OPCIONES)
    genero = models.CharField(max_length=50, choices=GENERO_OPCIONES)

    def __str__(self):
        return f"id:{self.id} - nombre:{self.nombre}"



class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20)
    fecha = models.DateTimeField(default=datetime.now)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto, through='VentaProducto')

    def __str__(self):
        return f"Venta {self.numero_factura} - Usuario: {self.usuario.username}"

class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
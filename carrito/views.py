from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Factura,PedidoEntregado
from .carrito_li import Carritos
from .forms import add_form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from carrito.models import Venta,VentaProducto
import uuid

def product_details(request, product_id):
    product = Producto.objects.get(id=product_id)
    data = {
        'nombre': product.nombre,
        'descripcion': product.descripcion,
        'precio': product.precio,
        'categoria': product.categoria,
        'marca': product.marca
        # Agrega aquí cualquier otro campo que necesites
    }
    return JsonResponse(data)

def search(request):
    # Check if the request is a post request.
    carrito=Carritos(request)
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        posts = Producto.objects.filter(descripcion__contains=search_query)
        return render(request, 'search.html', {'query':search_query, 'posts':posts,"carrito":carrito})
    else:
        return render(request, 'search.html',{})

@login_required
def listar_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas.html', {'ventas': ventas})



def pedidos_pendientes(request):
    pedidos = Factura.objects.filter(usuario=request.user, pendiente=True)
    if not pedidos.exists():
        print("No hay pedidos pendientes.")
    print(pedidos)
    return render(request, 'ver_compras.html', {'pedidos': pedidos})


# Vista para eliminar un pedido pendiente
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Factura, id=pedido_id, usuario=request.user, pendiente=True)
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver-compra')
    return render(request, 'eliminar_pedido.html', {'pedido': pedido})

def ver_compras(request):
    return render(request, 'ver_compras.html')



@login_required
def listar_pedidos_pendientes(request):
    usuario = request.user
    pedidos_pendientes = Factura.objects.filter(usuario=usuario, pendiente=True, entregado=False)
    return render(request, 'pedidos_pendientes.html', {'pedidos': pedidos_pendientes})

def compras_realizadas(request):
    return render(request, 'compra_exitosa.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Factura, PedidoEntregado, Venta, VentaProducto, Producto
from decimal import Decimal
from datetime import datetime

def entregar_pedido(request, factura_id, total):
    # Convertir total a Decimal
    total_decimal = Decimal(total)
    
    # Obtener la factura usando el ID
    factura = get_object_or_404(Factura, id=factura_id)
    
    # Mover la factura a la tabla histórica `PedidoEntregado`
    PedidoEntregado.objects.create(
        usuario=factura.usuario,
        numero_factura=factura.numero_factura,
        total=factura.total,
        fecha_entrega=datetime.now()  # Registrar la fecha de entrega
    )
    
    # Crear una venta para los productos asociados a la factura
    venta = Venta.objects.create(
        usuario=factura.usuario,
        numero_factura=factura.numero_factura,
        fecha=datetime.now(),
        total_pagado=total_decimal
    )
    
    carrito = request.session.get('carrito', {})
    print("Contenido del carrito en entregar_pedido:", carrito)  # Debugging

    for item in carrito.values():
        producto = Producto.objects.get(id=item['item_id'])
        VentaProducto.objects.create(
            venta=venta,
            producto=producto,
            cantidad=item['cantidad'],
            precio_unitario=item['precio'],
            total=item['total']
        )
    
    # Eliminar la factura de la tabla original `Factura`
    factura.delete()
    
    return redirect('listar_facturas')


def estado_cuenta_por_fecha(request):
    facturas = Factura.objects.filter(pendiente=True).order_by('fecha')
    return render(request, 'facturacion.html', {'facturas': facturas})

def anular_pedido(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    factura.delete()
    return redirect('listar_facturas')

def estado_cuenta_por_cliente(request):
    facturas = Factura.objects.filter(pendiente=True).order_by('usuario__username')
    return render(request, 'facturacion.html', {'facturas': facturas})

def listar_facturas(request):
    facturas_pendientes = Factura.objects.filter(pendiente=True, entregado=False)
    return render(request, 'facturacion.html', {'facturas': facturas_pendientes})

# def procesar_compra(request):
#         if request.method == 'POST':
#             # Obtener el usuario actual
#             usuario = request.user

#             # Generar un número de factura único
#             numero_factura = str(uuid.uuid4()).split('-')[0]

#             # Obtener el total de la compra
#             total_sum = sum(item['total'] for item in request.session['carrito'].values())

#             # Crear la factura y guardarla en la base de datos
#             factura = Factura.objects.create(
#                 usuario=usuario,
#                 numero_factura=numero_factura,
#                 total=total_sum,
#                 fecha=datetime.now()
#             )

#             # Limpiar el carrito después de la compra
#             request.session['carrito'] = {}

#             return redirect('compra_exitosa')  # Redirigir a una página de éxito
#         return redirect('carrito')  # Redirigir al carrito si algo sale mal

def agregar_carrito(request, item_id):
    item = Producto.objects.get(id=item_id)
    carrito = Carritos(request)
    resultado = carrito.agregar(item, int(request.GET.get('cantidad', 1)))
    
    return JsonResponse(resultado)

def eliminar_carrito(request, item_id):
    item = Producto.objects.get(id=item_id)
    carrito = Carritos(request)
    carrito.quitar(item)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carritos(request)
    carrito.limpiar()
    return redirect('carrito')

# Vista para mostrar la tienda con todos los productos
def tienda(request):
    carrito=Carritos(request)
    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'productos': productos, "carrito":carrito})

def restar(request, id):
    carrito = Carritos(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)

    # Obtener la cantidad de productos diferentes en el carrito (IDs únicos)
    cantidad_ids_unicos = len(carrito.carrito.keys())

    request.session["carrito_count"] -= 1
    return JsonResponse({'count': cantidad_ids_unicos})


def cart_count(request):
    carrito = Carritos(request)
    count = sum(item["cantidad"] for item in carrito.carrito.values())
    return JsonResponse({"count": count})    
# Vista para agregar un producto al carrito
def add(request, id):
    carrito = Carritos(request)
    producto = Producto.objects.get(id=id)
    cantidad = int(request.GET.get('cantidad', 1))
    carrito.agregar(producto, cantidad)

    # Obtener la cantidad de productos diferentes en el carrito (IDs únicos)
    cantidad_ids_unicos = len(carrito.carrito.keys())

    return JsonResponse({'count': cantidad_ids_unicos})
    
  # Redirige a la vista del carrito después de agregar
def guardar(request, id):
    carrito = Carritos(request)
    producto = get_object_or_404(Producto, id=id)
    
    cantidad = int(request.GET.get('cantidad', 1))  # Obtener la cantidad desde los parámetros de la URL
    
    for _ in range(cantidad):  # Agregar el producto la cantidad de veces especificada
        carrito.agregar(producto)
    
    total_items = sum(item["cantidad"] for item in carrito.carrito.values())
    return JsonResponse({'count': total_items})


# Vista para eliminar un producto del carrito
def eliminar_carrito(request, id):
    carrito = Carritos(request)
    producto = get_object_or_404(Producto, id=id)
    carrito.eliminar(producto)
    return redirect("carrito")  # Redirige a la vista del carrito después de eliminar

# Vista para mostrar el carrito de compras
def compras(request):
    carrito = request.session.get('carrito', {})
    total_sum = 0

    for key, item in carrito.items():
        total_sum += item['total']

    context = {
        'carrito': carrito,
        'total_sum': total_sum,
    }
    if request.method == 'POST':
        request.session['carrito_counter'] = 0
    return render(request, 'carrito.html', context)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tienda')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def account_manage(request):
    return render(request, 'account.html')

def admin_manager(request):
    prods = Producto.objects.all()
    return render(request, 'admin_manager.html',{"prod_list":prods})
    

def edit_dialog(request,id):
    table_prods = Producto.objects.all()
    prod = get_object_or_404(Producto,pk=id)
    if request.method == 'POST':
        form = add_form(request.POST,instance=prod)
        print("edited :" , prod)
        if form.is_valid():
            form.save()
             # test print
            return redirect('admin_manager')
    else:
        form = add_form()
    return render(request, 'edit_dialog.html',{"edit_form":form,"prod_list":table_prods})

def delete_dialog(request,id):
    table_prods = Producto.objects.all()
    prod = get_object_or_404(Producto,pk=id)
    if request.method == 'POST':
        print("deleted :" , prod)
        prod.delete()
        return redirect('admin_manager')
    
    return render(request, 'delete_dialog.html',{"prod_list":table_prods})


def add_dialog(request):
    table_prods = Producto.objects.all()
    if request.method == 'POST':
        form = add_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_manager')
    else:
        form = add_form()
    return render(request, 'add_dialog.html', {'add_form':add_form,"prod_list":table_prods})

def dialgo_back(request):
    return redirect('admin_manager')

def logout_dialog(request):
    logout(request)
    return render(request, 'logout_dialog.html')

def payment(request):
    return render(request, 'payment.html')


"""
URL configuration for mercado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include, re_path
from carrito import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('carrito/', views.compras, name="carrito"),
    path('tienda', views.tienda, name="tienda"),
    path('carrito/', include('paypal.standard.ipn.urls')),
    path('productos/', views.productos, name="productos"),
    
    path('admin_manager/', views.admin_manager, name="admin_manager"),
    path('agregar_carrito/<int:id>', views.guardar, name="agregar_carrito"),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar'),
    path('agregar/<int:id>', views.add, name="agregar"),
    path('restar/<int:id>', views.restar, name="restar"),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('admin_manager/edit/<int:id>', views.edit_dialog, name='edit_dialog'),
    path('admin_manager/delete/<int:id>', views.delete_dialog, name='delete_dialog'),
    path('admin_manager/add', views.add_dialog, name="add_dialog"),
    path('account/logout', views.logout_dialog, name='logout_dialog'),
    path('admin_manager/dialgo_back', views.dialgo_back, name="dialgo_back"),
    path('eliminar/<int:id>', views.eliminar_carrito, name="quitar"),
    # path('comprar/', views.procesar_compra, name='procesar_compra'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    re_path(r'^entregar_pedido/(?P<factura_id>\d+)/(?P<total>\d+(\.\d{1,2})?)/$', views.entregar_pedido, name='entregar_pedido'),
    path('estado_cuenta/fecha', views.estado_cuenta_por_fecha, name='estado_fecha'),
    path('estado_cuenta/cliente', views.estado_cuenta_por_cliente, name='estado_cliente'),
    path('anular_pedido/<int:factura_id>', views.anular_pedido, name='anular_pedido'),
    path('compra exitosa/',views.compras_realizadas ,name='compra_exitosa'),
    path('eliminar-pedido/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('ver compras/',views.pedidos_pendientes ,name='ver-compra'),
    path('mis-ventas/', views.listar_ventas, name='listar_ventas'),
    path('buscar/', views.search, name='buscar'),
    path('buscar-categoria/<str:cat>', views.search_by_cat, name='buscar_categoria'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),


    path('payment/', views.payment, name='payment'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('accounts/profile/',views.history,name="account"),
    path('accounts/profile/change_name',views.change_username_popup,name="change_username_dialog"),

    path('', include('PaymentApp.urls')),
    path('', include('paypal.standard.ipn.urls')),
]

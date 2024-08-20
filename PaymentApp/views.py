from django.shortcuts import render, redirect
from carrito.models import Producto, Factura
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from datetime import datetime

def CheckOut(request, total):
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': 'carrito de SportXpress',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs={'total': total})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'total': total})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'total': total,
        'paypal': paypal_payment
    }

    return render(request, 'checkout.html', context)

def PaymentSuccessful(request, total):
    if request.method == 'GET':
        usuario = request.user
        numero_factura = str(uuid.uuid4()).split('-')[0]

        # Asumimos que tienes un carrito en la sesión
        carrito = request.session.get('carrito', {})

        # Crear la factura y guardarla en la base de datos
        factura = Factura.objects.create(
            usuario=usuario,
            numero_factura=numero_factura,
            total=total,
            fecha=datetime.now(),
            products=",".join([f"{item['nombre']} (x{item['cantidad']})" for item in carrito.values()])
        )

        # Actualizar el stock de los productos
        for item in carrito.values():
            try:
                producto = Producto.objects.get(id=item['item_id'])
                producto.stock -= item['cantidad']
                producto.save()
            except Producto.DoesNotExist:
                # Manejar el caso en que el producto no existe
                pass

        # Limpiar el carrito después de la compra
        request.session.pop('carrito', None)

        return redirect('compra_exitosa')

    return render(request, 'payment-success.html', {'total': total})

def paymentFailed(request, total):
    return render(request, 'payment-failed.html', {'total': total})

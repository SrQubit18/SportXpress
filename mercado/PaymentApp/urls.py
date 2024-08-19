from django.urls import path , re_path
from . import views

urlpatterns = [
    re_path(r'^checkout/(?P<total>\d+(\.\d{1,2})?)/$', views.CheckOut, name='checkout'),
    re_path(r'payment-success/(?P<total>\d+(\.\d{1,2})?)/$', views.PaymentSuccessful, name='payment-success'),
    re_path(r'payment-failed/(?P<total>\d+(\.\d{1,2})?)/$', views.paymentFailed, name='payment-failed'),
]
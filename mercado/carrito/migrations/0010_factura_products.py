# Generated by Django 5.1 on 2024-08-16 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0009_venta_ventaproducto_venta_productos'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='products',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
    ]

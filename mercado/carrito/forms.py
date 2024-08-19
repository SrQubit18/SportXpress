from django import forms
from .models import Producto

class add_form(forms.ModelForm):
     class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'stock', 'categoria', 'marca' , 'tamaño' , 'genero']


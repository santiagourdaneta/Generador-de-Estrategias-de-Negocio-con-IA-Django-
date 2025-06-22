from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'sector', 'tamano', 'descripcion_negocio', 'recursos_disponibles']
        widgets = {
            'descripcion_negocio': forms.Textarea(attrs={'rows': 4}),
            'recursos_disponibles': forms.Textarea(attrs={'rows': 3}),
        }
        # Puedes personalizar mensajes de error si lo deseas
        # error_messages = {
        #     'nombre': {
        #         'required': "Por favor, ingresa el nombre de tu empresa.",
        #         'max_length': "El nombre es muy largo."
        #     },
        # }

    # Puedes añadir validaciones personalizadas aquí
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre de la empresa debe tener al menos 3 caracteres.")
        return nombre

    def clean_sector(self):
        sector = self.cleaned_data.get('sector').lower()
        # Una lista más robusta de sectores válidos, o una tabla en la DB
        sectores_validos = ['restaurante', 'tienda de ropa', 'consultoria', 'tecnologia', 'educacion', 'salud', 'servicios', 'manufactura']
        if sector not in sectores_validos:
            raise forms.ValidationError(f"El sector '{sector}' no es válido o no está soportado. Prueba con: {', '.join(sectores_validos)}")
        return sector
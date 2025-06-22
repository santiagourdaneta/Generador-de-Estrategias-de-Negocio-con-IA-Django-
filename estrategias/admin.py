from django.contrib import admin
from .models import Empresa, Estrategia # Importa tus modelos

# Registra tus modelos para que aparezcan en el panel de administración
admin.site.register(Empresa)
admin.site.register(Estrategia)

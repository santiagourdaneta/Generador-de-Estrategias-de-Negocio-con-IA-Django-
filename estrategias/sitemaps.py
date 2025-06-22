# estrategias/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse # Para obtener las URLs por su nombre

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily' # Con qué frecuencia cambia la página

    def items(self):
        # Aquí listamos los nombres de las URLs estáticas que queremos en el sitemap
        return ['estrategias:generar_estrategia', 'estrategias:listar_estrategias']

    def location(self, item):
        # Obtiene la URL real para cada elemento
        return reverse(item)

# Si quisieras incluir URLs dinámicas (ej. cada estrategia generada si fueran públicas)
# from .models import Estrategia
# class EstrategiaSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.8
#     def items(self):
#         return Estrategia.objects.all() # Todas las estrategias
#     def lastmod(self, obj):
#         return obj.fecha_generacion # La última vez que fue modificada
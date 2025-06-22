from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from estrategias.sitemaps import StaticViewSitemap
# Importa RedirectView para la redirección
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy # Para obtener la URL de forma segura

sitemaps = {
    'static': StaticViewSitemap,
    # 'estrategias_dinamicas': EstrategiaSitemap, # Si decidieras hacer tus estrategias públicas
}

urlpatterns = [
# Redirige la URL raíz a la página de generar estrategia
    path('', RedirectView.as_view(url=reverse_lazy('estrategias:generar_estrategia'), permanent=True)),
    # 'permanent=True' indica una redirección 301 (permanente)

    path('admin/', admin.site.urls),
    path('estrategias/', include('estrategias.urls')), # ¡Aquí conectamos las URLs de nuestra app!
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

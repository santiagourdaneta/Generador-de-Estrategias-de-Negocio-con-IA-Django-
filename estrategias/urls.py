from django.urls import path
from .views import GenerarEstrategiaView, ListarEstrategiasView, DetalleEstrategiaView

app_name = 'estrategias' # Esto es útil para referenciar las URLs fácilmente

urlpatterns = [
    path('generar/', GenerarEstrategiaView.as_view(), name='generar_estrategia'),
    path('lista/', ListarEstrategiasView.as_view(), name='listar_estrategias'),
    path('<int:estrategia_id>/', DetalleEstrategiaView.as_view(), name='detalle_estrategia'),
]
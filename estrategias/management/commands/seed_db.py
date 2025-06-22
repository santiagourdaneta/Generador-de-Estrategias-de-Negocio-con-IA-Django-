from django.core.management.base import BaseCommand
from estrategias.models import Empresa, Estrategia
import random
from datetime import timedelta
from django.utils import timezone

# Import PLN related parts to simulate better strategy generation
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- Load PLN models (once for the command execution) ---
# Wrap in try-except for robustness if models aren't downloaded
try:
    nlp = spacy.load("es_core_news_sm")
    try:
        spanish_stopwords = set(stopwords.words('spanish'))
    except LookupError:
        nltk.download('stopwords')
        spanish_stopwords = set(stopwords.words('spanish'))
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
except Exception as e:
    print(f"Warning: Could not load PLN models for seeding ({e}). Falling back to simpler strategy generation.")
    nlp = None
    spanish_stopwords = set()


# Reuse the strategy generation logic from views.py
# This ensures consistency with how your app generates strategies
def _generate_strategy_ia(empresa_data, nlp_model, stopwords_set):
    # This is a simplified version for seeding, focusing on varied output.
    # For full complexity, you'd replicate the exact logic from views.py
    nombre_empresa = empresa_data['nombre']
    sector_empresa = empresa_data['sector'].lower()
    tamano_empresa = empresa_data['tamano']
    descripcion_negocio = empresa_data['descripcion_negocio']
    recursos_disponibles = empresa_data['recursos_disponibles'] or ""

    estrategia_generada = ""
    impacto = ""
    tipo_elegido = ""

    keywords_descripcion = []
    if nlp_model:
        doc_descripcion = nlp_model(descripcion_negocio.lower())
        keywords_descripcion = [
            token.text for token in doc_descripcion
            if token.is_alpha and token.text not in stopwords_set
        ]

    # Basic logic for seeding diversity
    strategy_types = ['marketing', 'ventas', 'operaciones', 'digital', 'expansion', 'financiera']
    tipo_elegido = random.choice(strategy_types)

    if "online" in keywords_descripcion or "e-commerce" in keywords_descripcion:
        tipo_elegido = "digital"
    elif "local" in keywords_descripcion or "fisica" in keywords_descripcion:
        tipo_elegido = random.choice(['marketing', 'ventas'])

    base_strategy = f"Para la empresa '{nombre_empresa}' en el sector de '{sector_empresa}' ({tamano_empresa}), "

    if tipo_elegido == 'marketing':
        estrategia_generada = base_strategy + "sugerimos enfocarse en campañas de redes sociales y publicidad dirigida para aumentar la visibilidad de la marca."
        impacto = "Incremento de reconocimiento de marca y leads."
    elif tipo_elegido == 'ventas':
        estrategia_generada = base_strategy + "se recomienda optimizar el proceso de ventas con capacitación al equipo y programas de fidelización de clientes."
        impacto = "Mejora en la tasa de conversión y retención de clientes."
    elif tipo_elegido == 'operaciones':
        estrategia_generada = base_strategy + "la clave está en optimizar la cadena de suministro y los procesos internos para reducir costos y mejorar la eficiencia."
        impacto = "Reducción de gastos operativos y mejora de la calidad del servicio."
    elif tipo_elegido == 'digital':
        estrategia_generada = base_strategy + "prioriza la presencia online. Desarrolla un e-commerce robusto y utiliza SEO/SEM para atraer tráfico cualificado."
        impacto = "Expansión del mercado y nuevas fuentes de ingresos."
    elif tipo_elegido == 'expansion':
        estrategia_generada = base_strategy + "evalúa nuevas geografías o segmentos de mercado. Considera alianzas estratégicas o franquicias."
        impacto = "Crecimiento de la cuota de mercado y diversificación."
    elif tipo_elegido == 'financiera':
        estrategia_generada = base_strategy + "enfócate en la gestión de flujo de caja y la optimización de costes. Busca nuevas vías de financiación si es necesario."
        impacto = "Mayor estabilidad financiera y capacidad de inversión."

    return {
        'tipo_estrategia': tipo_elegido,
        'descripcion_estrategia': estrategia_generada,
        'impacto_estimado': impacto
    }


class Command(BaseCommand):
    help = 'Populates the database with sample data for Empresa and Estrategia models.'

    def handle(self, *args, **options):
        self.stdout.write("Deleting existing Empresa and Estrategia data...")
        Estrategia.objects.all().delete()
        Empresa.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        sectors = ['restaurante', 'tienda de ropa', 'consultoria', 'tecnologia', 'educacion', 'salud', 'servicios']
        sizes = ['micro', 'pequena', 'mediana']

        sample_businesses = [
            {
                'nombre': 'Cafetería del Sol',
                'sector': 'restaurante',
                'tamano': 'micro',
                'descripcion_negocio': 'Pequeña cafetería artesanal con enfoque en productos locales.',
                'recursos_disponibles': 'Buen local, equipo pequeño, bajo presupuesto.'
            },
            {
                'nombre': 'Moda Express',
                'sector': 'tienda de ropa',
                'tamano': 'pequena',
                'descripcion_negocio': 'Tienda de ropa juvenil con énfasis en tendencias rápidas. Buscando expandir online.',
                'recursos_disponibles': 'Inventario variado, poca presencia online.'
            },
            {
                'nombre': 'Consultores Alpha',
                'sector': 'consultoria',
                'tamano': 'mediana',
                'descripcion_negocio': 'Consultoría especializada en optimización de procesos para medianas empresas.',
                'recursos_disponibles': 'Equipo experto, amplia cartera de clientes.'
            },
            {
                'nombre': 'Tech Solutions Pro',
                'sector': 'tecnologia',
                'tamano': 'pequena',
                'descripcion_negocio': 'Desarrollo de software a medida para startups. Necesita visibilidad.',
                'recursos_disponibles': 'Equipo técnico fuerte, marketing limitado.'
            },
            {
                'nombre': 'Centro de Aprendizaje Creativo',
                'sector': 'educacion',
                'tamano': 'micro',
                'descripcion_negocio': 'Ofrece talleres de arte y música para niños. Busca más inscripciones.',
                'recursos_disponibles': 'Espacio adecuado, pasión por la enseñanza.'
            },
             {
                'nombre': 'Salud y Bienestar S.A.',
                'sector': 'salud',
                'tamano': 'mediana',
                'descripcion_negocio': 'Clínica de fisioterapia con 3 sucursales, buscando eficiencia operativa y crecimiento.',
                'recursos_disponibles': 'Personal cualificado, equipamiento moderno, necesidad de estandarizar procesos.'
            },
            {
                'nombre': 'Servicios Rápidos del Valle',
                'sector': 'servicios',
                'tamano': 'pequena',
                'descripcion_negocio': 'Empresa de limpieza y mantenimiento para oficinas y hogares. Compite por precio.',
                'recursos_disponibles': 'Buena base de clientes, necesidad de diferenciación.'
            },
            {
                'nombre': 'Panadería Tradición',
                'sector': 'restaurante', # Para probar otro del mismo sector
                'tamano': 'micro',
                'descripcion_negocio': 'Panadería artesanal con productos de horno tradicionales. Necesita marketing online.',
                'recursos_disponibles': 'Recetas únicas, lealtad de clientes mayores.'
            }
        ]

        created_count = 0
        for business_data in sample_businesses:
            empresa, created = Empresa.objects.get_or_create(
                nombre=business_data['nombre'],
                defaults={
                    'sector': business_data['sector'],
                    'tamano': business_data['tamano'],
                    'descripcion_negocio': business_data['descripcion_negocio'],
                    'recursos_disponibles': business_data['recursos_disponibles']
                }
            )
            if created:
                created_count += 1
            else:
                # Update if exists to ensure consistent data for seeding purposes
                empresa.sector = business_data['sector']
                empresa.tamano = business_data['tamano']
                empresa.descripcion_negocio = business_data['descripcion_negocio']
                empresa.recursos_disponibles = business_data['recursos_disponibles']
                empresa.save()

            # Generate strategy using the simulated AI logic
            strategy_info = _generate_strategy_ia(
                {
                    'nombre': empresa.nombre,
                    'sector': empresa.sector,
                    'tamano': empresa.tamano,
                    'descripcion_negocio': empresa.descripcion_negocio,
                    'recursos_disponibles': empresa.recursos_disponibles
                },
                nlp,
                spanish_stopwords
            )

            # Create strategy with a slightly varied date
            random_days = random.randint(0, 30)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            past_date = timezone.now() - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

            Estrategia.objects.create(
                empresa=empresa,
                tipo_estrategia=strategy_info['tipo_estrategia'],
                descripcion_estrategia=strategy_info['descripcion_estrategia'],
                impacto_estimado=strategy_info['impacto_estimado'],
                fecha_generacion=past_date # Assign a varied past date
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded strategy for {empresa.nombre}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(sample_businesses)} businesses and their strategies."))
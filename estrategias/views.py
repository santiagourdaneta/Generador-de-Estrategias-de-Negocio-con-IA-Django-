from django.shortcuts import render, redirect
from django.views import View
from .models import Empresa, Estrategia
from .forms import EmpresaForm # ¡Importamos nuestro formulario!
from django.http import JsonResponse
import json
import random

# Importaciones para PLN
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- Carga de modelos PLN (se ejecuta una sola vez al iniciar el servidor) ---
try:
    nlp = spacy.load("es_core_news_sm")
    # Descargar stopwords de NLTK si no están presentes
    try:
        spanish_stopwords = set(stopwords.words('spanish'))
    except LookupError:
        nltk.download('stopwords')
        spanish_stopwords = set(stopwords.words('spanish'))
    # Descargar punkt tokenizer de NLTK si no está presente
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

except Exception as e:
    print(f"Error al cargar modelos de PLN: {e}. Las funciones de PLN no estarán disponibles.")
    # Si hay un error al cargar, definimos nlp como None para evitar fallos.
    # Podrías considerar un mecanismo de fallback aquí.
    nlp = None
    spanish_stopwords = set()


# Función auxiliar para la lógica de generación de estrategia (para mantener el código limpio)
def generar_estrategia_ia(empresa_data, nlp_model, stopwords_set):
    nombre_empresa = empresa_data['nombre']
    sector_empresa = empresa_data['sector'].lower() # Convertir a minúsculas para consistencia
    tamano_empresa = empresa_data['tamano']
    descripcion_negocio = empresa_data['descripcion_negocio']
    recursos_disponibles = empresa_data['recursos_disponibles'] or "" # Asegurar que no sea None

    estrategia_generada = ""
    impacto = ""
    tipo_elegido = ""

    # --- Análisis de texto con spaCy y NLTK ---
    keywords_descripcion = []
    keywords_recursos = []
    tiene_desafio = False

    if nlp_model: # Solo si el modelo de PLN se cargó correctamente
        doc_descripcion = nlp_model(descripcion_negocio.lower())
        doc_recursos = nlp_model(recursos_disponibles.lower())

        keywords_descripcion = [
            token.text for token in doc_descripcion
            if token.is_alpha and token.text not in stopwords_set
        ]
        keywords_recursos = [
            token.text for token in doc_recursos
            if token.is_alpha and token.text not in stopwords_set
        ]

        # Detección de posibles desafíos (simulación de análisis de sentimiento básico)
        desafios_palabras = ['competencia', 'crisis', 'problema', 'bajas ventas', 'costos altos', 'escasez', 'retrasos']
        tiene_desafio = any(word in descripcion_negocio.lower() for word in desafios_palabras)

    # --- Lógica de generación de estrategias basada en reglas ---

    # Priorización de estrategias según el sector y tamaño
    if sector_empresa == 'restaurante':
        tipo_elegido = 'marketing' # Default para restaurante
        if 'delivery' in keywords_descripcion or 'envio' in keywords_descripcion or 'domicilio' in keywords_descripcion:
            tipo_elegido = 'operaciones'
            estrategia_generada = f"Para tu {tamano_empresa} restaurante, optimiza tu servicio de delivery. Mejora tiempos de entrega, invierte en empaques adecuados y promociona en plataformas populares. Considera alianzas estratégicas con servicios de entrega."
            impacto = "Aumento de pedidos a domicilio y expansión de la base de clientes."
        elif 'experiencia' in keywords_descripcion or 'ambiente' in keywords_descripcion or 'tematico' in keywords_descripcion:
            tipo_elegido = 'marketing'
            estrategia_generada = f"Para tu {tamano_empresa} restaurante, crea una experiencia culinaria única. Organiza noches temáticas, talleres de cocina o eventos con música en vivo. Usa redes sociales para mostrar el ambiente y los platos más atractivos."
            impacto = "Incremento de clientes en el local y mejora de la reputación de marca."
        else:
            estrategia_generada = f"Para tu {tamano_empresa} restaurante, céntrate en marketing local. Publica anuncios en medios comunitarios, participa en eventos del barrio y ofrece promociones especiales para atraer a residentes cercanos."
            impacto = "Mayor reconocimiento local y aumento del tráfico peatonal."

    elif sector_empresa == 'tienda de ropa':
        tipo_elegido = 'ventas' # Default para tienda de ropa
        if 'online' in keywords_descripcion or 'e-commerce' in keywords_descripcion or 'web' in keywords_descripcion:
            tipo_elegido = 'digital'
            estrategia_generada = f"Para tu {tamano_empresa} tienda de ropa, impulsa tu plataforma de e-commerce. Optimiza la experiencia de compra online, ofrece envíos rápidos y políticas de devolución claras, y utiliza publicidad digital segmentada."
            impacto = "Expansión del alcance de clientes a nivel nacional (o regional) y aumento de ventas online."
        elif 'boutique' in keywords_descripcion or 'exclusivo' in keywords_descripcion or 'diseno' in keywords_descripcion:
            tipo_elegido = 'marketing'
            estrategia_generada = f"Para tu {tamano_empresa} boutique de ropa, enfócate en marketing de exclusividad. Organiza eventos de lanzamiento de nuevas colecciones, colabora con influencers de moda y crea un programa de fidelización VIP."
            impacto = "Posicionamiento de marca de lujo/exclusiva y aumento del valor promedio de compra."
        else:
            estrategia_generada = f"Para tu {tamano_empresa} tienda de ropa, mejora la experiencia en tienda. Capacita a tu personal en ventas consultivas, organiza vitrinas atractivas y ofrece asesoría de imagen personalizada."
            impacto = "Incremento de la tasa de conversión en tienda y fidelización de clientes."

    elif sector_empresa == 'consultoria':
        tipo_elegido = 'ventas' # Default para consultoría
        if 'digital' in keywords_descripcion or 'tecnologia' in keywords_descripcion or 'software' in keywords_descripcion:
            tipo_elegido = 'marketing'
            estrategia_generada = f"Para tu {tamano_empresa} consultoría tecnológica, posiciona tu marca como líder de pensamiento. Crea blogs, webinars y estudios de caso que demuestren tu experiencia. Participa en conferencias y eventos del sector."
            impacto = "Atrae leads de alta calidad y establece autoridad en tu nicho."
        elif 'pymes' in keywords_descripcion or 'pequenas empresas' in keywords_descripcion:
            tipo_elegido = 'ventas'
            estrategia_generada = f"Para tu {tamano_empresa} consultoría enfocada en PYMES, desarrolla paquetes de servicios accesibles y claros. Ofrece talleres gratuitos o diagnósticos iniciales de bajo costo para captar clientes potenciales."
            impacto = "Aumento de la base de clientes PYME y generación de nuevas oportunidades."
        else:
            estrategia_generada = f"Para tu {tamano_empresa} consultoría, busca referencias y testimonios de clientes satisfechos. Crea un programa de incentivos por recomendaciones. Asiste a eventos de networking y ferias empresariales."
            impacto = "Crecimiento orgánico a través de la reputación y la confianza."

    else:
        # Estrategia genérica si el sector no está cubierto por reglas específicas
        tipo_elegido = random.choice(['marketing', 'ventas', 'operaciones', 'digital', 'expansion', 'financiera'])
        estrategia_generada = f"Para tu {tamano_empresa} empresa en el sector de '{sector_empresa}', una estrategia general sería: "
        if tiene_desafio:
            estrategia_generada += "primero, identifica y aborda los desafíos internos o externos que enfrentas. Realiza un análisis FODA. "
        estrategia_generada += "Luego, enfócate en mejorar tu presencia online (sitio web, redes sociales), optimizar tu propuesta de valor y fortalecer la relación con tus clientes existentes."
        impacto = "Mejora general del rendimiento del negocio y mayor resiliencia ante desafíos."

    # Lógica adicional basada en tamaño y recursos
    if tamano_empresa == 'micro':
        estrategia_generada += " Dada tu escala de microempresa, prioriza estrategias de bajo costo y alto impacto, como marketing de boca en boca, optimización de redes sociales orgánicas y colaboraciones locales."
        impacto += " Ideal para recursos limitados."
    elif tamano_empresa == 'pequena':
        estrategia_generada += " Como pequeña empresa, considera invertir en herramientas que automaticen tareas repetitivas y te permitan escalar, como un CRM sencillo o software de gestión de proyectos."
        impacto += " Permite un crecimiento más eficiente y mejor organización."

    if 'bajo presupuesto' in keywords_recursos or 'limitados recursos' in keywords_recursos:
        estrategia_generada += " Con un presupuesto ajustado, enfócate en estrategias de guerrilla marketing, maximiza el uso de herramientas gratuitas de análisis y promoción online, y busca alianzas estratégicas."
        impacto += " Optimización del retorno de inversión con recursos escasos."
    elif 'buen local' in keywords_recursos or 'ubicacion privilegiada' in keywords_recursos:
        estrategia_generada += " Aprovecha tu buen local para organizar eventos, exhibiciones o demostraciones de productos que atraigan a clientes y creen comunidad. Asegura una señalización clara y atractiva."
        impacto += " Aumento del tráfico en tienda y visibilidad local."
    elif 'equipo pequeno' in keywords_recursos or 'personal reducido' in keywords_recursos:
        estrategia_generada += " Con un equipo pequeño, la automatización y la delegación inteligente son clave. Capacita a tu personal en tareas multifuncionales y considera externalizar servicios no esenciales."
        impacto += " Maximización de la productividad del personal existente."
    elif 'experiencia tecnica' in keywords_recursos or 'conocimiento especializado' in keywords_recursos:
        estrategia_generada += " Capitaliza tu experiencia técnica/conocimiento especializado creando contenido de valor (blogs, videos, podcasts) y ofreciendo talleres o consultorías personalizadas para posicionarte como referente."
        impacto += " Posicionamiento como líder de la industria y atracción de clientes de alto valor."

    return {
        'tipo_estrategia': tipo_elegido,
        'descripcion_estrategia': estrategia_generada,
        'impacto_estimado': impacto
    }


# Vistas de la aplicación
class GenerarEstrategiaView(View):
    def get(self, request):
        # Muestra el formulario HTML inicial
        return render(request, 'estrategias/generar_estrategia.html')

    def post(self, request):
        data = {}
        try:
            # Intentar parsear como JSON (para cuando se integre con Vue/React)
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # Si no es JSON, asumir datos de formulario POST tradicional (para la demo HTML simple)
            data = request.POST.dict()

        # Instanciar el formulario con los datos recibidos
        form = EmpresaForm(data)

        if form.is_valid():
            # Si los datos son válidos, los obtenemos
            cleaned_data = form.cleaned_data

            # 1. Guardar la información de la empresa (o actualizar si ya existe)
            # Usamos get_or_create para evitar duplicados si el nombre ya existe
            empresa, created = Empresa.objects.get_or_create(
                nombre=cleaned_data['nombre'],
                defaults={
                    'sector': cleaned_data['sector'],
                    'tamano': cleaned_data['tamano'],
                    'descripcion_negocio': cleaned_data['descripcion_negocio'],
                    'recursos_disponibles': cleaned_data['recursos_disponibles']
                }
            )
            if not created:
                # Si la empresa ya existía, actualizamos sus datos
                empresa.sector = cleaned_data['sector']
                empresa.tamano = cleaned_data['tamano']
                empresa.descripcion_negocio = cleaned_data['descripcion_negocio']
                empresa.recursos_disponibles = cleaned_data['recursos_disponibles']
                empresa.save()

            # 2. Generar la estrategia usando la lógica de IA/ML
            estrategia_info = generar_estrategia_ia(
                {
                    'nombre': empresa.nombre,
                    'sector': empresa.sector,
                    'tamano': empresa.tamano,
                    'descripcion_negocio': empresa.descripcion_negocio,
                    'recursos_disponibles': empresa.recursos_disponibles
                },
                nlp, # Pasamos el modelo de PLN
                spanish_stopwords # Pasamos las stopwords
            )

            # 3. Guardar la estrategia generada en nuestra base de datos
            nueva_estrategia = Estrategia.objects.create(
                empresa=empresa,
                tipo_estrategia=estrategia_info['tipo_estrategia'],
                descripcion_estrategia=estrategia_info['descripcion_estrategia'],
                impacto_estimado=estrategia_info['impacto_estimado']
            )

            # 4. Devolver la estrategia al usuario como JSON
            return JsonResponse({
                'success': True,
                'estrategia_id': nueva_estrategia.id,
                'nombre_empresa': empresa.nombre,
                'tipo_estrategia': nueva_estrategia.tipo_estrategia,
                'descripcion_estrategia': nueva_estrategia.descripcion_estrategia,
                'impacto_estimado': nueva_estrategia.impacto_estimado
            })
        else:
            # Si los datos NO son válidos, devolvemos los errores del formulario
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class ListarEstrategiasView(View):
    def get(self, request):
        estrategias = Estrategia.objects.all().order_by('-fecha_generacion')
        return render(request, 'estrategias/listar_estrategias.html', {'estrategias': estrategias})


class DetalleEstrategiaView(View):
    def get(self, request, estrategia_id):
        try:
            estrategia = Estrategia.objects.get(id=estrategia_id)
        except Estrategia.DoesNotExist:
            estrategia = None # O podrías devolver un error 404
        return render(request, 'estrategias/detalle_estrategia.html', {'estrategia': estrategia})
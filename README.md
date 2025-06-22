
Este proyecto es un generador de estrategias de negocio inteligente diseñado para pequeñas y medianas empresas (PYMES). Utiliza Django como un backend robusto para manejar toda la lógica, la base de datos y la interfaz de usuario.

Características Principales
Generación Inteligente de Estrategias: Utiliza la descripción del negocio, el sector, el tamaño y los recursos disponibles para generar estrategias personalizadas de marketing, ventas, operaciones o digital.
PLN Básico: Emplea librerías como NLTK y SpaCy para extraer palabras clave y realizar un análisis de "sentimiento" básico, adaptando las estrategias a desafíos o fortalezas detectadas.
Lógica Basada en Reglas: Un motor de reglas interno que define estrategias específicas para diferentes sectores y escenarios de negocio.
Gestión de Estrategias: Guarda las estrategias generadas en una base de datos para su consulta posterior.
Interfaz de Usuario Simple: La interfaz de usuario se renderiza directamente desde las plantillas de Django, usando HTML, CSS y JavaScript básico para la interactividad.
Validaciones Robustas: Incluye validaciones tanto en el frontend (JavaScript) para feedback instantáneo, como en el backend (formularios de Django) para garantizar la integridad de los datos.
SEO Básico: Configuración de django.contrib.sitemaps para una mejor indexación por motores de búsqueda.
Seeder de Datos: Incluye un comando de gestión de Django para poblar rápidamente la base de datos con datos de ejemplo para desarrollo y pruebas.

Requisitos
Python 3.8+
pip (Administrador de paquetes de Python)

Configuración y Ejecución
Sigue estos pasos para poner en marcha el proyecto:

1. Clonar el Repositorio (si aplica)
Bash

git clone https://github.com/santiagourdaneta/Generador-de-Estrategias-de-Negocio-con-IA-Django-/
cd Generador-de-Estrategias-de-Negocio-con-IA-Django-

2. Configuración del Backend (Django)
Crear y Activar Entorno Virtual:

Bash

python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

Instalar Dependencias de Python:

Bash

pip install -r requirements.txt

Descargar Modelos de PLN (NLTK y SpaCy):

Bash

python -m spacy download es_core_news_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

Realizar Migraciones de Base de Datos:

Bash

python manage.py makemigrations
python manage.py migrate

Crear un Superusuario (Opcional, para acceder al Admin de Django):

Bash

python manage.py createsuperuser

Sembrar Datos de Ejemplo (Opcional, pero recomendado para desarrollo):

Bash

python manage.py seed_db

Ejecutar el Servidor de Django
Asegúrate de que tu entorno virtual esté activado.
Navega al Directorio Raíz del Proyecto (Generador-de-Estrategias-de-Negocio-con-IA-Django-/ donde está manage.py).
Iniciar el Servidor de Django:
Bash

python manage.py runserver
El servidor de Django se ejecutará en http://127.0.0.1:8000/.

Uso de la Aplicación
Acceder a la Aplicación: Abre tu navegador y ve a http://127.0.0.1:8000/. Serás redirigido a la página para generar estrategias.
Generar una Estrategia: Rellena el formulario con la información de la empresa y haz clic en "Generar Estrategia".
Ver Estrategias Guardadas: Navega a http://127.0.0.1:8000/estrategias/lista/ para ver el historial de estrategias generadas.
Administración de Django: Accede al panel de administración en http://127.0.0.1:8000/admin/ (usando el superusuario que creaste) para gestionar los modelos de Empresa y Estrategia.

Próximos Pasos y Mejoras (Roadmap)
Interfaz de Usuario Mejorada: Aunque no se usa un framework de JS, se puede mejorar el HTML/CSS/JS de las plantillas de Django para una experiencia más rica y responsiva.
Autenticación de Usuarios: Implementar un sistema de registro y login para usuarios.
Modelos de IA/ML Avanzados: Explorar la integración con APIs de modelos de lenguaje grandes (LLMs) como Google Gemini o OpenAI (con un plan de uso adecuado) para una generación de estrategias más sofisticada.
Dashboard de Usuario: Una interfaz personalizada para que los usuarios gestionen sus empresas y estrategias guardadas.
Exportación de Estrategias: Funcionalidad para exportar estrategias en PDF o DOCX.
Historial de Cambios: Permitir a los usuarios editar y guardar diferentes versiones de una estrategia.

from django.db import models

# Este es el modelo para guardar la información de una Empresa
class Empresa(models.Model):
    nombre = models.CharField(max_length=200) # Nombre de la empresa (texto corto)
    sector = models.CharField(max_length=100) # Tipo de negocio (e.g., "restaurante", "tienda de ropa")
    tamano = models.CharField(max_length=50, choices=[ # Tamaño de la empresa (opciones predefinidas)
        ('micro', 'Microempresa'),
        ('pequena', 'Pequeña Empresa'),
        ('mediana', 'Mediana Empresa'),
    ])
    descripcion_negocio = models.TextField() # Una descripción más larga de lo que hace el negocio
    recursos_disponibles = models.TextField(blank=True, null=True) # Qué recursos tiene la empresa (opcional)
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Cuando se registró esta empresa

    def __str__(self):
        return self.nombre # Para que se muestre bonito en el panel de administración

# Este es el modelo para guardar las Estrategias que nuestro amigo mágico sugiere
class Estrategia(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) # A qué empresa pertenece esta estrategia
    tipo_estrategia = models.CharField(max_length=100, choices=[ # Tipo de estrategia (e.g., "marketing", "operaciones")
        ('marketing', 'Marketing'),
        ('ventas', 'Ventas'),
        ('operaciones', 'Operaciones'),
        ('expansion', 'Expansión'),
        ('digital', 'Digitalización'),
        ('financiera', 'Financiera'),
    ])
    descripcion_estrategia = models.TextField() # Detalles de la estrategia
    impacto_estimado = models.TextField(blank=True, null=True) # Qué se espera lograr con la estrategia (opcional)
    fecha_generacion = models.DateTimeField(auto_now_add=True) # Cuando se generó esta estrategia

    def __str__(self):
        return f"Estrategia para {self.empresa.nombre} ({self.tipo_estrategia})"
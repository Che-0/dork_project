from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Ej: Documentos, Bases de Datos, Directorios")
    descripcion = models.TextField(blank=True, null=True, help_text="Breve descripción de la categoría")

    def __str__(self):
        return self.nombre

class Dork(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='dorks')
    titulo = models.CharField(max_length=150, help_text="Ej: Buscar respaldos SQL")
    # La plantilla usará {target} donde deba ir el dominio o palabra clave validada por tu regex
    plantilla = models.CharField(max_length=255, help_text="Ej: site:{target} (ext:sql OR ext:bak)")
    explicacion = models.TextField(blank=True, null=True, help_text="¿Para qué sirve este dork exactamente?")
    
    def __str__(self):
        return f"[{self.categoria.nombre}] - {self.titulo}"
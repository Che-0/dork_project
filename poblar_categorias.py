import os
import django

# 1. Configurar el entorno de Django para poder usar los modelos
# Reemplaza 'dork_project' con el nombre exacto de la carpeta que contiene tu settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dork_project.settings')
django.setup()

# 2. Importar el modelo (debe hacerse después de django.setup())
from generator.models import Categoria

def poblar_db():
    categorias = [
        {
            "nombre": "Archivos Sensibles y Documentos",
            "descripcion": "Encuentra PDFs, hojas de cálculo o documentos que contienen palabras clave como 'confidencial', 'salario' o 'uso interno'."
        },
        {
            "nombre": "Listados de Directorios",
            "descripcion": "Busca servidores mal configurados que muestran su estructura de carpetas (Directory Listing)."
        },
        {
            "nombre": "Paneles de Administración y Logins",
            "descripcion": "Descubre portales de acceso, paneles de administrador y páginas de inicio de sesión que no deberían estar indexadas."
        },
        {
            "nombre": "Configuración y Credenciales",
            "descripcion": "Búsquedas para encontrar archivos .env, .sql, .log o .config que exponen contraseñas y cadenas de conexión."
        },
        {
            "nombre": "Subdominios y Reconocimiento",
            "descripcion": "Utiliza comodines y exclusiones (ej. site:*.ejemplo.com -www) para mapear la infraestructura y descubrir entornos de desarrollo."
        },
        {
            "nombre": "Cámaras y Dispositivos",
            "descripcion": "Orientado a encontrar hardware expuesto a internet, como cámaras web o dispositivos IoT indexados por error."
        }
    ]

    print("Iniciando la carga de categorías...")
    
    for cat_data in categorias:
        # get_or_create evita que se dupliquen si ejecutas el script más de una vez
        categoria, creada = Categoria.objects.get_or_create(
            nombre=cat_data["nombre"],
            defaults={"descripcion": cat_data["descripcion"]}
        )
        
        if creada:
            print(f"✅ Creada: {categoria.nombre}")
        else:
            print(f"ℹ️ Ya existía: {categoria.nombre}")

    print("¡Base de datos poblada con éxito!")

if __name__ == '__main__':
    poblar_db()
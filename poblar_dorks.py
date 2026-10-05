import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dork_project.settings')
django.setup()

from generator.models import Categoria, Dork

def poblar_dorks():
    categorias = {cat.nombre: cat for cat in Categoria.objects.all()}
    
    if not categorias:
        print("❌ Error: Ejecuta poblar_categorias.py primero.")
        return

    dorks_data = [
        # 1. Archivos Sensibles y Documentos
        {
            "categoria": "Archivos Sensibles y Documentos",
            "titulo": "Documentos Confidenciales",
            "plantilla": "site:{target} (ext:pdf OR ext:doc OR ext:docx) intext:\"confidencial\" OR intext:\"uso interno\"",
            "explicacion": "Rastrea documentos ofimáticos indexados que contengan etiquetas de confidencialidad."
        },
        {
            "categoria": "Archivos Sensibles y Documentos",
            "titulo": "Datos Financieros y Presupuestos",
            "plantilla": "site:{target} (ext:xls OR ext:xlsx OR ext:csv) intitle:\"presupuesto\" OR intitle:\"reporte\" OR intext:\"salario\"",
            "explicacion": "Localiza hojas de cálculo que puedan exponer finanzas o datos de nómina."
        },
        {
            "categoria": "Archivos Sensibles y Documentos",
            "titulo": "Correos Electrónicos Expuestos",
            "plantilla": "site:{target} intext:\"@gmail.com\" OR intext:\"@yahoo.com\" OR intext:\"@hotmail.com\"",
            "explicacion": "Filtra páginas dentro del dominio que contengan direcciones de correo electrónico genéricas."
        },

        # 2. Listados de Directorios
        {
            "categoria": "Listados de Directorios",
            "titulo": "Directorios Raíz Expuestos",
            "plantilla": "site:{target} intitle:\"index of /\"",
            "explicacion": "Detecta servidores web (Apache/Nginx) mal configurados que listan su estructura de carpetas."
        },
        {
            "categoria": "Listados de Directorios",
            "titulo": "Carpetas de Respaldos (Backups)",
            "plantilla": "site:{target} intitle:\"index of\" inurl:backup OR inurl:bak",
            "explicacion": "Identifica directorios abiertos que específicamente almacenan copias de seguridad."
        },
        {
            "categoria": "Listados de Directorios",
            "titulo": "Directorios de Código Fuente",
            "plantilla": "site:{target} intitle:\"index of\" (inurl:src OR inurl:source OR inurl:includes)",
            "explicacion": "Busca carpetas que exponen el código fuente o los 'includes' de la aplicación web."
        },

        # 3. Paneles de Administración y Logins
        {
            "categoria": "Paneles de Administración y Logins",
            "titulo": "Páginas de Login Genéricas",
            "plantilla": "site:{target} inurl:login OR inurl:signin OR intitle:\"iniciar sesión\"",
            "explicacion": "Encuentra puntos de acceso para usuarios o administradores."
        },
        {
            "categoria": "Paneles de Administración y Logins",
            "titulo": "Paneles de WordPress",
            "plantilla": "site:{target} inurl:wp-admin OR inurl:wp-login.php",
            "explicacion": "Identifica instalaciones de WordPress y sus portales de administración."
        },
        {
            "categoria": "Paneles de Administración y Logins",
            "titulo": "Portales de Bases de Datos",
            "plantilla": "site:{target} inurl:phpmyadmin OR intitle:\"phpMyAdmin\"",
            "explicacion": "Detecta interfaces de gestión de bases de datos expuestas al público."
        },

        # 4. Configuración y Credenciales
        {
            "categoria": "Configuración y Credenciales",
            "titulo": "Variables de Entorno (.env)",
            "plantilla": "site:{target} ext:env OR ext:txt inurl:.env",
            "explicacion": "Busca archivos de entorno que contienen tokens de API, contraseñas y configuraciones sensibles."
        },
        {
            "categoria": "Configuración y Credenciales",
            "titulo": "Volcados de Bases de Datos (SQL)",
            "plantilla": "site:{target} (ext:sql OR ext:dump OR ext:bak) intext:\"INSERT INTO\" OR intext:\"CREATE TABLE\"",
            "explicacion": "Rastrea respaldos de bases de datos indexados por error."
        },
        {
            "categoria": "Configuración y Credenciales",
            "titulo": "Archivos de Logs con Contraseñas",
            "plantilla": "site:{target} ext:log intext:\"password\" OR intext:\"error\"",
            "explicacion": "Busca archivos de registro del servidor que puedan estar filtrando credenciales en texto plano."
        },
        {
            "categoria": "Configuración y Credenciales",
            "titulo": "Llaves Privadas SSH/RSA",
            "plantilla": "site:{target} ext:pem OR ext:key OR ext:txt intext:\"BEGIN RSA PRIVATE KEY\"",
            "explicacion": "Identifica certificados o llaves privadas expuestas."
        },

        # 5. Subdominios y Reconocimiento
        {
            "categoria": "Subdominios y Reconocimiento",
            "titulo": "Mapeo de Subdominios (Excluyendo WWW)",
            "plantilla": "site:*.{target} -www",
            "explicacion": "Lista subdominios asociados al objetivo, filtrando el sitio web principal."
        },
        {
            "categoria": "Subdominios y Reconocimiento",
            "titulo": "Entornos de Desarrollo y Pruebas",
            "plantilla": "site:*.{target} inurl:dev OR inurl:test OR inurl:staging",
            "explicacion": "Busca subdominios utilizados para desarrollo, que suelen tener menos controles de seguridad."
        },
        {
            "categoria": "Subdominios y Reconocimiento",
            "titulo": "Búsqueda de Repositorios Git Expuestos",
            "plantilla": "site:{target} inurl:/.git/config OR ext:git",
            "explicacion": "Identifica si la carpeta oculta de control de versiones ha sido indexada."
        },

        # 6. Cámaras y Dispositivos
        {
            "categoria": "Cámaras y Dispositivos",
            "titulo": "Cámaras IP Genéricas",
            "plantilla": "site:{target} inurl:view/view.shtml OR inurl:view/index.shtml",
            "explicacion": "Busca interfaces de visualización de cámaras IP de red."
        },
        {
            "categoria": "Cámaras y Dispositivos",
            "titulo": "Dispositivos IoT y Routers",
            "plantilla": "site:{target} intitle:\"RouterOS router configuration\" OR intitle:\"Cisco Systems\"",
            "explicacion": "Detecta paneles de configuración de infraestructura de red."
        }
    ]

    print("Iniciando la carga de Dorks...")
    
    for data in dorks_data:
        cat_obj = categorias.get(data["categoria"])
        if cat_obj:
            dork, creado = Dork.objects.get_or_create(
                categoria=cat_obj,
                titulo=data["titulo"],
                defaults={
                    "plantilla": data["plantilla"],
                    "explicacion": data["explicacion"]
                }
            )
            if creado:
                print(f"✅ Dork Creado: {dork.titulo}")
            else:
                print(f"ℹ️ Ya existía: {dork.titulo}")
        else:
            print(f"⚠️ Advertencia: Categoría '{data['categoria']}' no encontrada para el dork '{data['titulo']}'")

    print("¡Base de datos de Dorks poblada con éxito!")

if __name__ == '__main__':
    poblar_dorks()
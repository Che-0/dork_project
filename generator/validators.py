# generator/validators.py
import re

def extraer_dominio(texto):
    """
    Busca y extrae un dominio válido de una cadena de texto o URL.
    Ejemplo: 'https://www.ejemplo.com/ruta' -> 'ejemplo.com'
    """
    # Patrón para limpiar URLs y quedarse solo con el host
    patron_url = r'(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    
    coincidencia = re.search(patron_url, texto)
    if coincidencia:
        # Retorna el grupo 1, que es el dominio limpio
        return coincidencia.group(1)
    return None

def es_ip_valida(texto):
    """
    Verifica si el texto ingresado es una dirección IPv4 válida.
    Útil si quieres hacer dorks que apunten a IPs.
    """
    patron_ip = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    if re.match(patron_ip, texto):
        return True
    return False

def sanitizar_palabras_clave(texto):
    """
    Limpia cadenas de búsqueda (intext o inurl) eliminando caracteres
    que podrían romper la sintaxis de Google o causar inyecciones.
    Permite letras, números, espacios, guiones y puntos.
    """
    # Sustituye cualquier cosa que NO sea (^) alfanumérico (\w), espacio (\s), punto (\.) o guion (\-)
    texto_limpio = re.sub(r'[^\w\s\.\-]', '', texto)
    
    # Elimina espacios múltiples
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
    
    return texto_limpio.strip()
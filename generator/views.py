# generator/views.py
from django.shortcuts import render
import urllib.parse
from .forms import DorkGeneratorForm
from .models import Dork
from .validators import extraer_dominio, sanitizar_palabras_clave

def index(request):
    dorks_generados = []
    target_limpio = ""
    categoria_seleccionada = None

    if request.method == 'POST':
        form = DorkGeneratorForm(request.POST)
        
        if form.is_valid():
            categoria = form.cleaned_data['categoria']
            target_raw = form.cleaned_data['target']
            palabras_extra_raw = form.cleaned_data.get('palabras_extra', '')
            excluir_terminos_raw = form.cleaned_data.get('excluir_terminos', '')

            categoria_seleccionada = categoria.nombre

            # 1. Validar el target principal
            dominio = extraer_dominio(target_raw)
            if dominio:
                target_limpio = dominio
            else:
                target_limpio = sanitizar_palabras_clave(target_raw)

            # 2. Procesar filtros adicionales
            filtros_adicionales = ""
            
            if palabras_extra_raw:
                # Sanitiza y añade comillas para forzar la coincidencia exacta
                palabras_limpias = sanitizar_palabras_clave(palabras_extra_raw)
                filtros_adicionales += f' "{palabras_limpias}"'
            
            if excluir_terminos_raw:
                # Divide por espacios o comas, sanitiza y añade el operador '-'
                terminos = excluir_terminos_raw.replace(',', ' ').split()
                for t in terminos:
                    t_limpio = sanitizar_palabras_clave(t)
                    if t_limpio:
                        filtros_adicionales += f' -"{t_limpio}"'

            # 3. Generar Dorks
            plantillas = Dork.objects.filter(categoria=categoria)

            for dork in plantillas:
                # Reemplaza el objetivo y concatena los filtros adicionales al final
                dork_base = dork.plantilla.format(target=target_limpio)
                dork_texto = f"{dork_base}{filtros_adicionales}".strip()
                
                dork_url = urllib.parse.quote_plus(dork_texto) 
                
                dorks_generados.append({
                    'titulo': dork.titulo,
                    'explicacion': dork.explicacion,
                    'dork_texto': dork_texto,
                    'link_google': f"https://www.google.com/search?q={dork_url}"
                })
    else:
        form = DorkGeneratorForm()

    context = {
        'form': form,
        'dorks_generados': dorks_generados,
        'target_limpio': target_limpio,
        'categoria_seleccionada': categoria_seleccionada
    }
    
    return render(request, 'generator/index.html', context)
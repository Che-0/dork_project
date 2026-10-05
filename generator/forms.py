# generator/forms.py
from django import forms
from .models import Categoria

class DorkGeneratorForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
        label="Categoría de Búsqueda"
    )
    
    target = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: miempresa.com o "término objetivo"'
        }),
        label="Objetivo (Dominio o Texto)",
        help_text="Ingresa el objetivo principal para generar el Dork."
    )
    
    palabras_extra = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: admin, reportes'
        }),
        label="Palabras Clave Adicionales",
        help_text="Términos extra que DEBEN aparecer."
    )
    
    excluir_terminos = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: blog, foro, public'
        }),
        label="Términos a Excluir",
        help_text="Términos que NO deben aparecer (se añadirán con '-')."
    )
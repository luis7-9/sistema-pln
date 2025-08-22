# analisis/views.py
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
from collections import Counter
import re

def upload_file(request):
    """
    Maneja la subida de archivos y genera un histograma de palabras.
    
    Si el método de la solicitud es POST, procesa el archivo subido.
    De lo contrario, muestra un formulario de subida.
    """
    histogram = None
    file_name = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file_instance = form.save()
            
            file_path = uploaded_file_instance.file.path
            file_name = uploaded_file_instance.file.name.split('/')[-1]

            # Leer el contenido del archivo
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            except UnicodeDecodeError:
                # Si falla la decodificación, intenta con otra
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()
                except Exception as e:
                    return render(request, 'analisis/upload.html', {
                        'form': form,
                        'error_message': f'Error al leer el archivo: {e}'
                    })

            # Generar el histograma
            # Convertir a minúsculas y limpiar el texto de puntuación
            cleaned_text = re.sub(r'[^\w\s]', '', text_content.lower())
            words = cleaned_text.split()
            word_counts = Counter(words)
            
            # Ordenar las palabras por frecuencia de forma descendente
            histogram = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
            
    else:
        form = UploadFileForm()

    return render(request, 'analisis/upload.html', {
        'form': form,
        'histogram': histogram,
        'file_name': file_name
    })



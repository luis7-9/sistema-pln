# analisis/views.py
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
from collections import Counter
import re
import os

# Lista de stopwords en español (predefinida)
STOPWORDS_ES = {
    "a", "acá", "ahí", "al", "algo", "algún", "alguna", "algunas", "alguno", "algunos",
    # ... existing code ...
    "voy", "vuestra", "vuestras", "vuestro", "vuestros", "y", "ya"
}

def upload_file(request):
    """
    Maneja la subida de archivos y permite acciones de usuario:
    - 'histogram': genera histograma (tabla Palabra/Frecuencia).
    - 'process': aplica limpieza y muestra el texto limpio en una caja.
    - 'uppercase': convierte a MAYÚSCULAS y muestra el texto en una caja.
    - 'lowercase': convierte a minúsculas y muestra el texto en una caja.
    """
    histogram = None
    file_name = None
    tokens = None
    file_id = None
    transformed_text = None  # texto a mostrar en una sola caja

    if request.method == 'POST':
        action = request.POST.get('action')

        # Subir archivo
        if action == 'upload':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file_instance = form.save()
                file_id = uploaded_file_instance.id
                file_name = os.path.basename(uploaded_file_instance.file.name)
            else:
                return render(request, 'analisis/upload.html', {'form': form})

        # Generar histograma (tabla Palabra/Frecuencia)
        elif action == 'histogram':
            form = UploadFileForm()
            file_id = request.POST.get('file_id')
            if not file_id:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'No se recibió el identificador del archivo para generar el histograma.'
                })
            try:
                uploaded_file_instance = UploadedFile.objects.get(id=file_id)
                file_name = os.path.basename(uploaded_file_instance.file.name)
                file_path = uploaded_file_instance.file.path

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()

                words = text_content.split()
                word_counts = Counter(words)
                histogram = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

            except UploadedFile.DoesNotExist:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'El archivo no existe o fue eliminado.'
                })

        # Convertir texto a MAYÚSCULAS y mostrar en caja
        elif action == 'uppercase':
            form = UploadFileForm()
            file_id = request.POST.get('file_id')
            if not file_id:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'No se recibió el identificador del archivo para convertir a mayúsculas.'
                })
            try:
                uploaded_file_instance = UploadedFile.objects.get(id=file_id)
                file_name = os.path.basename(uploaded_file_instance.file.name)
                file_path = uploaded_file_instance.file.path

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()

                transformed_text = text_content.upper()

            except UploadedFile.DoesNotExist:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'El archivo a procesar no existe o ya fue eliminado.'
                })

        # Convertir texto a minúsculas y mostrar en caja
        elif action == 'lowercase':
            form = UploadFileForm()
            file_id = request.POST.get('file_id')
            if not file_id:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'No se recibió el identificador del archivo para convertir a minúsculas.'
                })
            try:
                uploaded_file_instance = UploadedFile.objects.get(id=file_id)
                file_name = os.path.basename(uploaded_file_instance.file.name)
                file_path = uploaded_file_instance.file.path

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()

                transformed_text = text_content.lower()

            except UploadedFile.DoesNotExist:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'El archivo a procesar no existe o ya fue eliminado.'
                })

        # Procesamiento con limpieza (minúsculas, sin puntuación, sin stopwords) y mostrar en caja
        elif action == 'process':
            form = UploadFileForm()
            file_id = request.POST.get('file_id')
            if not file_id:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'No se recibió el identificador del archivo para procesar.'
                })
            try:
                uploaded_file_instance = UploadedFile.objects.get(id=file_id)
                file_name = os.path.basename(uploaded_file_instance.file.name)
                file_path = uploaded_file_instance.file.path

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()

                cleaned_text = re.sub(r'[^\w\s]', '', text_content.lower())
                words = cleaned_text.split()
                tokens = [w for w in words if w and w not in STOPWORDS_ES]
                transformed_text = " ".join(tokens)

            except UploadedFile.DoesNotExist:
                return render(request, 'analisis/upload.html', {
                    'form': form,
                    'error_message': 'El archivo a procesar no existe o ya fue eliminado.'
                })

        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()

    return render(request, 'analisis/upload.html', {
        'form': form,
        'file_name': file_name,
        'file_id': file_id,
        'transformed_text': transformed_text,
        'histogram': histogram
    })
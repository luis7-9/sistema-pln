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
    "ante", "antes", "así", "aun", "aunque", "bien", "cabe", "cada", "casi", "como", "con",
    "contra", "cual", "cuales", "cuando", "cuanto", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ello", "ellos", "en", "entre", "era", "eras", "ereis",
    "eramos", "eran", "eres", "es", "esa", "esas", "ese", "esos", "esta", "estas", "este",
    "estos", "etc", "fin", "fue", "fueron", "fui", "ha", "hace", "hacen", "hacer", "hacemos",
    "haciendo", "hacia", "hago", "hasta", "hay", "he", "hecho", "hemos", "hizo", "la", "las",
    "lo", "los", "me", "menos", "mi", "mía", "mías", "mío", "míos", "mis", "muy", "nada",
    "ni", "no", "nos", "nosotras", "nosotros", "o", "para", "pero", "poco", "por", "porque",
    "que", "quien", "quienes", "se", "sea", "sean", "si", "sido", "siempre", "siendo", "sin",
    "sino", "solo", "somos", "soy", "su", "sus", "tal", "tampoco", "tan", "tanta", "tantas",
    "tanto", "tantos", "te", "tenemos", "tengo", "ti", "tiempo", "tiene", "tienen", "todo",
    "todos", "un", "una", "uno", "unos", "va", "vamos", "van", "voy", "vuestra", "vuestras",
    "vuestro", "vuestros", "y", "ya"
}


def generate_ngrams(tokens, n):
    """
    Genera n-gramas a partir de una lista de tokens.
    """
    if len(tokens) < n:
        return []
    ngrams_list = [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
    return ngrams_list


def upload_file(request):
    """
    Maneja la subida de archivos y permite acciones de usuario.
    """
    histogram = None
    file_name = None
    file_id = None
    transformed_text = None
    ngrams_data = None
    error_message = None
    n_value = None  # Para mostrar el valor de n en la plantilla

    if request.method == 'POST':
        action = request.POST.get('action')
        file_id = request.POST.get('file_id')

        # Subir archivo
        if action == 'upload':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file_instance = form.save()
                file_id = uploaded_file_instance.id
                file_name = os.path.basename(uploaded_file_instance.file.name)
            else:
                return render(request, 'analisis/upload.html', {'form': form})

        # Procesar y generar resultados
        else:
            form = UploadFileForm()
            if not file_id:
                error_message = 'No se recibió el identificador del archivo.'
            else:
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

                    # Consolidación del preprocesamiento
                    cleaned_text = re.sub(r'[^\w\s]', '', text_content.lower())
                    words = cleaned_text.split()
                    tokens = [w for w in words if w and w not in STOPWORDS_ES]

                    if action == 'histogram':
                        word_counts = Counter(words)
                        histogram = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

                    elif action == 'uppercase':
                        transformed_text = text_content.upper()

                    elif action == 'lowercase':
                        transformed_text = text_content.lower()

                    elif action == 'process':
                        transformed_text = " ".join(tokens)

                    elif action == 'ngramas':
                        n_value_str = request.POST.get('n_value', '2')
                        try:
                            n_value = int(n_value_str)
                            if n_value < 1: n_value = 1
                        except (ValueError, TypeError):
                            n_value = 2  # Valor por defecto en caso de error

                        ngrams = generate_ngrams(tokens, n=n_value)
                        ngrams_counts = Counter(ngrams)
                        ngrams_data = sorted(ngrams_counts.items(), key=lambda item: item[1], reverse=True)

                except UploadedFile.DoesNotExist:
                    error_message = 'El archivo no existe o fue eliminado.'

    else:
        form = UploadFileForm()

    return render(request, 'analisis/upload.html', {
        'form': form,
        'file_name': file_name,
        'file_id': file_id,
        'transformed_text': transformed_text,
        'histogram': histogram,
        'ngrams_data': ngrams_data,
        'n_value': n_value,
        'error_message': error_message
    })
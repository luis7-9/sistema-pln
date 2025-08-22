# analisis/admin.py
from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """
    Clase para registrar el modelo UploadedFile en el panel de administración.
    """
    list_display = ('file', 'uploaded_at',)
    list_filter = ('uploaded_at',)
    search_fields = ('file',)



# analisis/models.py
from django.db import models

class UploadedFile(models.Model):
    """
    Modelo para almacenar los archivos subidos por el usuario.
    """
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Representación en cadena del modelo.
        """
        return f"Archivo subido: {self.file.name}"



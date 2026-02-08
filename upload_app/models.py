from django.db import models

class FileUpload(models.Model):
    """
    Stores an uploaded file with its upload timestamp.
    """

    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
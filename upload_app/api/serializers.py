from rest_framework import serializers
from upload_app.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    
    """
    Serializer for creating and representing FileUpload instances.
    """

    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']

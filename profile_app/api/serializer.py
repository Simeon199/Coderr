from rest_framework import serializers
from profile_app.models import BusinessProfile, CustomerProfile
# from django.contrib.auth import get_user_model

# User = get_user_model

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type"
        )

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = (
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type"
        )
from rest_framework import serializers
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class BusinessSerializer(serializers.ModelSerializer):
    
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type"
        ]
        read_only_fields = fields

class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "type"
        ]
        read_only_fields = fields

class BusinessProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating BusinessProfile data.
    """
    class Meta:
        model = BusinessProfile
        fields = [
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours"
        ]
        
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for reading BusinessProfile data with all user information
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    email =serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.created_at", read_only=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at"
        ]
        read_only_fields = fields

class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating CustomerProfile data.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "first_name",
            "last_name",
            "file",
            "user"
        ]

        # All fields are optional for partial updates
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for reading CustomerProfile data with all user information
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    email =serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.created_at", read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = fields
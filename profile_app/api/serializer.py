from rest_framework import serializers
from profile_app.models import BusinessProfile, CustomerProfile

class CustomerSerializer(serializers.ModelSerializer):
    """List view for customer profiles"""
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.CharField(source="user.file", read_only=True)
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

class BusinessSerializer(serializers.ModelSerializer):
    """List view for customer profiles"""
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.CharField(source="user.file", read_only=True)
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

class BusinessProfileUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for business profiles"""
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    file = serializers.CharField(source="user.file", required=False)
    location = serializers.CharField(required=False)
    tel = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    working_hours = serializers.CharField(required=False)

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
    
    def update(self, instance, validated_data):
        user_data = {}
        business_data = {}
        validated_user = validated_data.get("user", {})

        for field in ["first_name", "last_name", "file"]:
            if field in validated_user:
                user_data[field] = validated_user.pop(field)

        for field in ["location", "tel", "description", "working_hours"]:
            if field in validated_data:
                business_data[field] = validated_data.pop(field)

        # Update user fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()


        # Update business fields
        for attr, value in business_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    location = serializers.CharField(read_only=True)
    tel = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    working_hours = serializers.CharField(read_only=True)
    file = serializers.CharField(source="user.file", read_only=True)
    created_at = serializers.DateTimeField(source="user.created_at", read_only=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "created_at"
        ]
        read_only_fields = fields

class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for customer profiles"""
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    file = serializers.CharField(source="user.file", required=False)

    class Meta:
        model = CustomerProfile
        fields = [
            "first_name",
            "last_name",
            "file"
        ]

    def update(self, instance, validated_data):
        user_data = {}
        validated_user = validated_data.get("user", {})
        for field in ["first_name", "last_name", "file"]:
            if field in validated_user:
                user_data[field] = validated_user.pop(field)

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return instance

class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    """Detail view for individual customer profile"""
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.CharField(source="user.file", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(source="user.created_at", read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "email",
            "type",
            "created_at",
        ]
        read_only_fields = fields
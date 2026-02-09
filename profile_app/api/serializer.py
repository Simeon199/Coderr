from rest_framework import serializers
from profile_app.models import BusinessProfile, CustomerProfile
from upload_app.models import FileUpload


def get_file_url(user):
    """
    Return the file URL for a user's uploaded file, or None.
    """
    
    if user.file and user.file.file:
        return user.file.file.url
    return None


class CustomerSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing customer profiles.
    Exposes user-related fields via nested source lookups.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()
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

    def get_file(self, obj):
        return get_file_url(obj.user)


class BusinessSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing business profiles.
    Exposes user-related fields via nested source lookups.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()
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

    def get_file(self, obj):
        return get_file_url(obj.user)


class BusinessProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating business profiles.
    Handles updating both user-level and profile-level fields.
    """

    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.EmailField(source="user.email", required=False)
    file = serializers.FileField(required=False, allow_null=True)
    location = serializers.CharField(required=False)
    tel = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    working_hours = serializers.CharField(required=False)

    class Meta:
        model = BusinessProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "file",
            "location",
            "tel",
            "description",
            "working_hours"
        ]

    def _update_user_fields(self, instance, validated_data):
        """
        Extract and apply user-level fields (first_name, last_name)
        from validated data to the related user instance.
        """

        validated_user = validated_data.get("user", {})
        for field in ["first_name", "last_name", "email"]:
            if field in validated_user:
                setattr(instance.user, field, validated_user[field])

        uploaded_file = validated_data.get("file")
        if uploaded_file:
            file_upload = FileUpload.objects.create(file=uploaded_file)
            instance.user.file = file_upload

        instance.user.save()

    def _update_business_fields(self, instance, validated_data):
        """
        Extract and apply business-level fields from validated data
        to the profile instance.
        """

        for field in ["location", "tel", "description", "working_hours"]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

    def update(self, instance, validated_data):
        """
        Update both user-level and business-level fields for the profile.
        """

        self._update_user_fields(instance, validated_data)
        self._update_business_fields(instance, validated_data)
        return instance


class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single business profile with full detail.
    Includes all user and profile fields.
    """

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
    file = serializers.SerializerMethodField()
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

    def get_file(self, obj):
        return get_file_url(obj.user)


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating customer profiles.
    Handles updating user-level fields (first_name, last_name, file).
    """

    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.EmailField(source="user.email", required=False)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "file"
        ]

    def update(self, instance, validated_data):
        """
        Update user-level fields for the customer profile.
        """
        validated_user = validated_data.get("user", {})
        for field in ["first_name", "last_name", "email"]:
            if field in validated_user:
                setattr(instance.user, field, validated_user[field])

        uploaded_file = validated_data.get("file")
        if uploaded_file:
            file_upload = FileUpload.objects.create(file=uploaded_file)
            instance.user.file = file_upload

        instance.user.save()
        return instance


class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single customer profile with full detail.
    Includes all user fields and timestamps.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()
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

    def get_file(self, obj):
        return get_file_url(obj.user)
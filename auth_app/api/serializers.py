from rest_framework import serializers
from django.contrib.auth import authenticate
from auth_app.models import CustomUser
from rest_framework.authtoken.models import Token
from profile_app.models import CustomerProfile, BusinessProfile
from upload_app.models import FileUpload

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and creation of new users with type selection.
    """
    email = serializers.EmailField(required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
            'type': {'required': True}
        }

    def validate(self, data):
        """Ensure passwords match and that username and email are unique."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        return data
    
    def create(self, validated_data):
        """Create the user, the matching profile and an auth token."""
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type=validated_data['type']
        )
        if user.type == 'customer':
            CustomerProfile.objects.create(user=user)
        else:
            BusinessProfile.objects.create(user=user)
        Token.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Handles validation of user credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Authenticate the user with the provided username and password."""
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError({'error': 'Unable to log in with provided credentials.'})
        else:
            raise serializers.ValidationError('Must include "username" and "password"')
        attrs['user'] = user
        return attrs
    
class RegistrationResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration response.
    Returns token, username, email, and user_id.
    """
    token = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['token', 'username', 'email', 'user_id']
        read_only_fields = ['token', 'username', 'email', 'user_id']

    def get_token(self, obj):
        """Return the auth token key for the given user."""
        token = Token.objects.get(user=obj)
        return token.key
    
def get_file_url(user):
    """Return the file URL for a user's uploaded file, or None."""
    if user.file and user.file.file:
        return user.file.file.url
    return None


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profile data.
    """
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')
    file = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = ['user', 'username', 'type', 'first_name', 'last_name', 'file', 'type']

    def get_file(self, obj):
        return get_file_url(obj.user)


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for business profile data.
    """
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')
    file = serializers.SerializerMethodField()

    class Meta:
        model = BusinessProfile
        fields = ['user', 'username', 'type', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_file(self, obj):
        return get_file_url(obj.user)
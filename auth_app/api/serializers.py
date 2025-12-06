from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Serializes all fields for the User model.
    """
    class Meta:
        model = UserProfile
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and creation of new users.
    """
    username = serializers.CharField()
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields =  ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        self._validate_passwords(data)
        self._validate_email(data['email'])
        return data
    
    def _validate_passwords(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
    
    def _validate_email(self, email):
        if UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
    def create(self, validated_data):
        user = UserProfile(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
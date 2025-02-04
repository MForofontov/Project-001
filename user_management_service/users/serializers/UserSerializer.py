from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model() # This will refer to CustomUser due to AUTH_USER_MODEL setting in settings.py

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model to be serialized
        model = User
        # Define the fields to include in the serialized output
        fields = ('id', 'email', 'password')
        # Specify that the password field should be write-only
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        # Create a new user instance using the validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # Return the created user instance
        return user
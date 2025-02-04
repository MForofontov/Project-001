from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model() # This will refer to CustomUser due to AUTH_USER_MODEL setting in settings.py

class UserProfileSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be serialized
    class Meta:
        # Specify the model to be serialized
        model = User
        # Define the fields to include in the serialized output
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address']


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model() # This will refer to CustomUser due to AUTH_USER_MODEL setting in settings.py

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Call the parent class's get_token method to get the default token
        token = super().get_token(user)
        # Add custom claims here if needed
        return token

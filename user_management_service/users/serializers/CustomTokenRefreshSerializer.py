from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import serializers

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom serializer to handle refreshing JWT tokens.
    This serializer extends the TokenRefreshSerializer from the djangorestframework-simplejwt package.
    """
    def validate(self, attrs):
        """
        Validate the refresh token and return the new access token.

        Parameters
        ----------
        attrs : dict
            The input data containing the refresh token.

        Returns
        -------
        dict
            A dictionary containing the new access token and refresh token.
        """
        refresh_token = attrs.get('refresh')
        if not refresh_token:
            raise serializers.ValidationError({'refresh': 'No refresh token provided'})
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise serializers.ValidationError({'refresh': 'Invalid or expired refresh token'})
        except InvalidToken:
            raise serializers.ValidationError({'refresh': 'Blacklisted refresh token'})

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    raise serializers.ValidationError({'refresh': 'Failed to blacklist refresh token'})

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

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
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data
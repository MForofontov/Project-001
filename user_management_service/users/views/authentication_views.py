from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from users.serializers.CustomTokenRefreshSerializer import CustomTokenRefreshSerializer
from users.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from typing import Any

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh JWT tokens using a refresh token stored in cookies.
    """
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handles POST requests to refresh JWT tokens.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A response containing the new JWT tokens and setting them in cookies.
        """
        # Retrieve the refresh token from cookies
        refresh_token: str = request.COOKIES.get('refreshToken')
        if not refresh_token:
            # Return an error response if the refresh token is missing
            return Response({'message': 'Refresh token missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the serializer with the refresh token
        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            # Validate the serializer data
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Create a response indicating failure
            response: Response = Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # Delete the access and refresh tokens from cookies
            response.delete_cookie('accessToken')
            response.delete_cookie('refreshToken')
            
            return response

        # Create a response with the validated data
        response = Response(serializer.validated_data)
        # Retrieve the new access token from the validated data
        access_token: str = serializer.validated_data.get('access')

        # Set the new access token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )

        # Remove the refresh and access tokens from the response data
        response.data.pop('refresh', None)
        response.data.pop('access', None)

        # Return the response
        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens (access and refresh) and store them in cookies.
    """
    # Specify the custom serializer class to use
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handles POST requests to obtain JWT tokens and store them in cookies.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A response containing the JWT tokens and setting them in cookies.
        """
        # Initialize the serializer with the request data
        serializer: CustomTokenObtainPairSerializer = self.get_serializer(data=request.data)
        # Validate the serializer data
        serializer.is_valid(raise_exception=True)
        # Create a response with the validated data
        response: Response = Response(serializer.validated_data)

        # Retrieve the refresh and access tokens from the validated data
        access_token: str = serializer.validated_data['access']
        refresh_token: str = serializer.validated_data['refresh']

        # Set the access token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['ACCESS_COOKIE'],
            value=access_token,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        # Set the refresh token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=refresh_token,
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        )

        # Remove the refresh and access tokens from the response data
        response.data.pop('refresh', None)
        response.data.pop('access', None)

        # Return the response
        return response

class LogoutView(APIView):
    """
    View to handle user logout by deleting JWT tokens from cookies.
    """
    # Require the user to be authenticated to access this view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handles POST requests to log out the user by deleting JWT tokens from cookies.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A response indicating successful logout.
        """
        # Create a response indicating successful logout
        response: Response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        # Delete the access and refresh tokens from cookies
        response.delete_cookie(settings.SIMPLE_JWT['ACCESS_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        # Return the response
        return response

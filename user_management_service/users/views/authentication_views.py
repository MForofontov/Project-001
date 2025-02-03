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
    Custom view to handle refreshing JWT tokens and storing them in cookies.
    This view extends the TokenRefreshView from the djangorestframework-simplejwt package.
    """
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request: HttpRequest) -> Response:
        """
        Handle POST requests to refresh JWT tokens.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        *args : Any
            Additional positional arguments.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        Response
            A JSON response with the refreshed JWT tokens or an error message.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the validated data (tokens)
        tokens = serializer.validated_data

        # Create the response object
        response = Response(status=status.HTTP_200_OK)

        # Set the cookies for access and refresh tokens
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens['access'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        # Set the refresh token in cookies if rotation is enabled
        if tokens.get('refresh'):
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
                value=tokens['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            )

        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens (access and refresh) and store them in cookies.
    """
    # Specify the custom serializer class to use
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: HttpRequest) -> HttpResponse:
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
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the validated data (tokens)
        tokens = serializer.validated_data

        # Create the response object
        response = Response(status=status.HTTP_200_OK)

        # Set the access token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['ACCESS_COOKIE'],
            value=tokens['access'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        # Set the refresh token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=tokens['refresh'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        )

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

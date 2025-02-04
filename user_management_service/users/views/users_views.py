from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from users.models import CustomUser
from users.celery_tasks.send_verification_email import send_verification_email
from django.conf import settings
from typing import Dict

# Import the user model
User = get_user_model()

class UserRegistrationView(APIView):
    """
    View to create a new user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> Response:
        """
        Handles POST requests to create a new user.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        Response
            A response containing the serialized user data and a 201 Created status.
        """
        # Check if the user already exists
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'User with this email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the serializer with the request data
        serializer = UserSerializer(data=request.data)
        # Validate the data and raise an exception if invalid
        serializer.is_valid(raise_exception=True)
        # Save the validated data to create a new user
        user = serializer.save()
        
        # If the user is created successfully, send an email verification link
        send_verification_email.delay(user.id)

        # Generate tokens using the custom serializer
        token_serializer = CustomTokenObtainPairSerializer(data={'email': email, 'password': request.data.get('password')})
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        # Include tokens in the response data
        response_data = serializer.data
        response_data['tokens'] = tokens

        # Create the response object
        response = Response(response_data, status=status.HTTP_201_CREATED)

        # Set the access token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['ACCESS_COOKIE'],
            value=tokens['access'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        )
        # Set the refresh token in cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=tokens['refresh'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        )

        # Return the response
        return response

class UserProfileView(APIView):
    """
    View to retrieve and update the profile of the authenticated user.
    """
    # Require the user to be authenticated to access this view
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        """
        Handles GET requests to retrieve the profile of the authenticated user.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        Response
            A response containing the serialized user profile data and a 200 OK status.
        """
        # Get the authenticated user
        user: CustomUser = request.user
        # Serialize the user data
        serializer: UserProfileSerializer = UserProfileSerializer(user)
        # Return the serialized data with a 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        """
        Handles POST requests to update the profile of the authenticated user.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        Response
            A response containing the serialized updated user profile data and a 200 OK status,
            or a response containing validation errors and a 400 Bad Request status.
        """
        # Get the authenticated user
        user: CustomUser = request.user
        # Get the serializer with the request data and allow partial updates
        serializer: UserProfileSerializer = UserProfileSerializer(user, data=request.data, partial=True)
        # Check if the provided data is valid
        if serializer.is_valid():
            # Save the validated data to update the user profile
            serializer.save()
            # Return the serialized data with a 200 OK status
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return validation errors with a 400 Bad Request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserStatusView(APIView):
    """
    View to check if the user is authenticated.
    """
    # Require the user to be authenticated to access this view
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests to check if the user is authenticated.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A response indicating the user is authenticated.
        """
        # Return a response indicating the user is authenticated
        return Response({"message": "User is authenticated"}, status=status.HTTP_200_OK)

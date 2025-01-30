import requests
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
from django.views import View
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Optional

class GoogleLoginView(View):
    """
    View to handle the initial step of Google OAuth login.
    Redirects the user to Google's OAuth 2.0 authorization endpoint.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests to initiate Google OAuth login.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A redirect response to Google's OAuth 2.0 authorization endpoint.
        """
        google_auth_url: str = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            "response_type=code&"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
            "scope=email%20profile"
        )
        return HttpResponseRedirect(google_auth_url)

class GoogleCallbackView(View):
    """
    View to handle the callback from Google OAuth.
    Exchanges the authorization code for access and refresh tokens,
    retrieves user information, and generates JWT tokens.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the Google OAuth callback.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            A redirect response to the frontend dashboard with JWT tokens set as HTTP-only cookies.
        """
        code: str = request.GET.get('code')
        token_url: str = "https://oauth2.googleapis.com/token"
        token_data: dict = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        token_response: requests.Response = requests.post(token_url, data=token_data)
        token_json: dict = token_response.json()
        access_token: Optional[str] = token_json.get('access_token')
        google_refresh_token: Optional[str] = token_json.get('refresh_token')
        user_info_url: str = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_params: dict = {'access_token': access_token}
        user_info_response: requests.Response = requests.get(user_info_url, params=user_info_params)
        user_info: dict = user_info_response.json()

        email: Optional[str] = user_info.get('email')
        first_name: Optional[str] = user_info.get('given_name')
        last_name: Optional[str] = user_info.get('family_name')

        # Check if user exists, create if not
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name,
                      'last_name': last_name,
                      'registration_method': 'google',
                      'is_email_verified': True}
        )

        # Store the Google refresh token in the user's profile or another secure location
        user.google_refresh_token = google_refresh_token
        user.save()

        # Generate JWT tokens using RefreshToken
        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token_jwt: str = str(refresh.access_token)
        refresh_token_jwt: str = str(refresh)

        # Create response and set HTTP-only cookies for access and refresh tokens
        response: HttpResponse = HttpResponseRedirect('https://localhost/dashboard')  # Replace with your frontend URL
        response.set_cookie(
            key=settings.SIMPLE_JWT['ACCESS_COOKIE'],
            value=access_token_jwt,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=refresh_token_jwt,
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        )
        response.set_cookie('googleRefreshToken', google_refresh_token, httponly=True, secure=False, samesite='Lax')

        return response

class RefreshGoogleTokenView(View):
    """
    View to handle refreshing the Google access token using the Google refresh token.
    Generates new JWT tokens and sets them as HTTP-only cookies.
    """
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles POST requests to refresh the Google access token.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        JsonResponse
            A JSON response indicating the result of the token refresh operation.
        """
        user: CustomUser = request.user
        google_refresh_token: str = user.google_refresh_token

        token_url: str = "https://oauth2.googleapis.com/token"
        token_data: dict = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'refresh_token': google_refresh_token,
            'grant_type': 'refresh_token'
        }
        token_response: requests.Response = requests.post(token_url, data=token_data)

        if token_response.status_code == 200:
            token_json: dict = token_response.json()
            new_google_access_token: Optional[str] = token_json.get('access_token')

            # Generate new JWT tokens using the new Google access token
            refresh: RefreshToken = RefreshToken.for_user(user)
            access_token_jwt: str = str(refresh.access_token)
            refresh_token_jwt: str = str(refresh)

            # Create response and set HTTP-only cookies for access and refresh tokens
            response: JsonResponse = JsonResponse({'message': 'Tokens refreshed'})
            response.set_cookie('accessToken', access_token_jwt, httponly=True, secure=False, samesite='Lax')
            response.set_cookie('refreshToken', refresh_token_jwt, httponly=True, secure=False, samesite='Lax')
        else:
            # Create response indicating failure and clear the access and refresh tokens from cookies
            response = JsonResponse({'message': 'Failed to refresh tokens'}, status=400)
            response.delete_cookie('accessToken')
            response.delete_cookie('refreshToken')
            response.delete_cookie('googleRefreshToken')

        return response

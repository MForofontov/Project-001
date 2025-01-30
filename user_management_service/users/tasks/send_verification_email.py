from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.models import CustomUser
from users.tokens.email_verification_token import email_verification_token

@shared_task
def send_verification_email(user_id):
    """
    Sends a verification email to the user.

    Parameters
    ----------
    user_id : int
        The ID of the user to send the verification email to.
    """
    try:
        # Retrieve the user object using the provided user ID
        user = CustomUser.objects.get(pk=user_id)

        # Generate a token for email verification
        token = email_verification_token._make_hash_value(user)
        
        # Encode the user's ID in a URL-safe base64 format
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construct the verification link
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
        
        # Define the email subject
        subject = "Verify your email address"
        
        # Render the email message using an HTML template
        message = render_to_string('email_verification.html', {
            'user': user,
            'verification_link': verification_link,
        })
        
        # Send the email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist
        pass

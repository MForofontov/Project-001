import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for email verification.
    
    This class extends Django's PasswordResetTokenGenerator to create tokens
    for email verification purposes. The token is generated using the user's
    primary key, a timestamp, and the user's email confirmation status.
    """
    def _make_hash_value(self, user):
        """
        Generate a hash value to be used in the token.

        Parameters
        ----------
        user : CustomUser
            The user for whom the token is being generated.

        Returns
        -------
        str
            A string representing the hash value.
        """
        return (
            str(user.pk) + str(time.time()) + str(user.is_email_verified)
        )

    def has_token_expired(self, user, token):
        """
        Check if the token has expired.

        Parameters
        ----------
        user : CustomUser
            The user for whom the token was generated.
        token : str
            The token to check for expiration.

        Returns
        -------
        bool
            True if the token has expired, False otherwise.
        """
        try:
            # Extract the timestamp from the token
            timestamp = self._get_timestamp(token)
            # Calculate the expiration date (assuming 1 day expiration)
            expiration_date = datetime.fromtimestamp(timestamp) + timedelta(days=1)
            # Check if the current date and time is greater than the expiration date
            return datetime.now() > expiration_date
        except Exception:
            # Return False if there is an exception (e.g., invalid token format)
            return False

    def _get_timestamp(self, token):
        """
        Extract the timestamp from the token.

        Parameters
        ----------
        token : str
            The token from which to extract the timestamp.

        Returns
        -------
        int
            The timestamp extracted from the token.
        """
        try:
            # Split the token to get the timestamp part (base 36 encoded)
            ts_b36, _ = token.split("-")
            # Convert the base 36 encoded timestamp to an integer
            return int(ts_b36, 36)
        except ValueError:
            # Return None if there is a ValueError (e.g., invalid token format)
            return None

# Create an instance of the EmailVerificationTokenGenerator
email_verification_token = EmailVerificationTokenGenerator()
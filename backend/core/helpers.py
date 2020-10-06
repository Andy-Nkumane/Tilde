from rest_framework.authtoken.models import Token
import re
from core.constants import BUSINESS_EMAIL_DOMAIN
from django.contrib.auth import get_user_model

User = get_user_model()


def get_auth_token_for_email(email):
    """given a specific email address, fetch (or maybe create) a user then return a token if the user (now) exists. Users will only be created if the email address is an @Umuzi address"""
    assert "@" in email, f"This is not a valid email address: '{email}'"

    if email.endswith(f"@{BUSINESS_EMAIL_DOMAIN}"):
        first_name, last_name = get_first_and_last_names_from_business_email(email)
        user, user_created = User.objects.get_or_create(
            email=email, defaults={"first_name": first_name, "last_name": last_name}
        )
        token = Token.objects.get_or_create(user=user)[0]
        return token, user_created

    else:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None, False
        token = Token.objects.get_or_create(user=user)[0]
        return token, False


def get_first_and_last_names_from_business_email(email):
    assert email.endswith(f"@{BUSINESS_EMAIL_DOMAIN}"), f"Invalid email"

    first_name, last_name = re.search(
        f"(.*)\.(.*)@{BUSINESS_EMAIL_DOMAIN}", email
    ).groups()

    return first_name.capitalize(), last_name.capitalize()
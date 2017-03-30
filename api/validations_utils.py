import exceptions_utils
import messages
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status


def email_validation(data):
    try:
        email = data['email']
    except KeyError:
        raise exceptions_utils.ValidationException(messages.REQUIRED_EMAIL, status.HTTP_400_BAD_REQUEST)
    try:
        validate_email(email)
        data['email'] = email.lower()
        return data
    except ValidationError:
        raise exceptions_utils.ValidationException(messages.INVALID_EMAIL_ADDRESS, status.HTTP_400_BAD_REQUEST)


def password_validation(data):
    try:
        password = data['password']
        if password is None or not re.match(r'[A-Za-z0-9@#$%^&+=]+', password):
            raise exceptions_utils.ValidationException(messages.PASSWORD_NECESSITY, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return data
    except KeyError:
        raise exceptions_utils.ValidationException(messages.REQUIRED_PASSWORD, status.HTTP_400_BAD_REQUEST)

import exceptions_utils
import messages
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status

from api.models import User


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


def user_validation(pk):
    try:
        user = User.objects.get(pk=pk)
        return user
    except User.DoesNotExist:
        raise exceptions_utils.ValidationException(messages.USER_DOES_NOT_EXISTS, status.HTTP_404_NOT_FOUND)


def user_token_validation(token_user_id, pk):
    if int(pk) != token_user_id:
        raise exceptions_utils.ValidationException(messages.TOKEN_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED)


def user_validation_with_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        raise exceptions_utils.ValidationException(messages.USER_WITH_EMAIL_DOES_NOT_EXISTS, status.HTTP_404_NOT_FOUND)

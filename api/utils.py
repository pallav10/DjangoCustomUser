import hashlib
import random

import datetime
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token
from django.template.loader import get_template
from django.conf import settings
from api import messages
from api.models import User, UserResetPassword
from serializers import UserSerializer, UserProfileSerializer
import exceptions_utils
from rest_framework import status


def generate_token(user):
    # Token table is of Django Rest Framework
    # Creates the token at registration time
    token = Token.objects.create(user=user)
    # Return only the key with is associated with the object
    return token.key


def fetch_token(user):
    try:
        # Get the goal for the specified user and return key
        token = Token.objects.get(user_id=user.id)
        return token.key
    except Token.DoesNotExist:
        raise exceptions_utils.ValidationException(messages.TOKEN_NOT_FOUND, status.HTTP_404_NOT_FOUND)


def hash_password(password):
    return make_password(password)


def create_user(data):
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        token = Token.objects.create(user=user)
        keys = ['id', 'first_name', 'last_name', 'email', 'contact_no', 'created'
                ]  # data that we want to return as JSON response
        user_response = {k: v for k, v in user_serializer.data.iteritems() if k in keys}
        user_response['token'] = token.key
        return user_response
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_user(data, user):
    user_serializer = UserProfileSerializer(data=data, instance=user)
    if user_serializer.is_valid():
        user_serializer.save()
        return user_serializer.data
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


def authenticate_user(user, data):
    if user:
        token = fetch_token(user)
        user_serializer = UserProfileSerializer(user, data=data)
        if user_serializer.is_valid():
            keys = ['id', 'email']
            user_serializer_dict = {k: v for k, v in user_serializer.data.iteritems() if k in keys}
            user_serializer_dict['token'] = token
            user_serializer_dict.update(messages.LOGIN_SUCCESSFUL)
            return user_serializer_dict
        else:
            raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
    else:
        raise exceptions_utils.ValidationException(messages.INVALID_EMAIL_OR_PASSWORD, status.HTTP_401_UNAUTHORIZED)


def change_password(current_password, new_password, user):
    if user.check_password(current_password):

        if current_password != new_password:
            user.set_password(new_password)
            user.is_password_changed = True
            user.save()
            resp = {'user_id': user.id}
            resp.update(messages.PASSWORD_CHANGED)
            return resp
        else:
            raise exceptions_utils.ValidationException(messages.SAME_PASSWORD, status.HTTP_406_NOT_ACCEPTABLE)
    else:
        raise exceptions_utils.ValidationException(messages.CURRENT_PASSWORD_INCORRECT,
                                                   status.HTTP_401_UNAUTHORIZED)


def create_reset_password_key(email):
    user = User.objects.get(email=email)
    try:
        user_reset_password = UserResetPassword.objects.get(users_id=user.id)
        user_reset_password.delete()
    except UserResetPassword.DoesNotExist:
        pass
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    key = hashlib.sha1(salt + email).hexdigest()
    from django.utils import timezone
    key_expires = timezone.now() + datetime.timedelta(days=1)
    user_reset_password = UserResetPassword(users=user, key=key, key_expires=key_expires)
    user_reset_password.save()
    return key


def send_reset_password_mail(user, key, domain):
    url_body = "http://%s/api/users/%s/password_reset/confirm/%s" % (
        domain, user.id, key)
    html_template = get_template('password_reset_email_template.html')
    content_passed_to_template = ({'url_body': url_body})
    html_content = html_template.render(content_passed_to_template)
    send_email = EmailMessage(
        'Password Reset',
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    send_email.content_subtype = "html"
    send_email.send()


def reset_password(user_reset_password, password):
    if user_reset_password:
        pk = user_reset_password.users_id
        user = User.objects.get(id=pk)
        user.set_password(password)
        # user.is_reset_password = True
        user.save()
        response = 'Password changed successfully! :)'
    else:
        response = 'Link is not valid. :('
    return response

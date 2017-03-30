from rest_framework import serializers
from models import User


# used for registration, it hold the value of user table with all fields.


class UserSerializer(serializers.ModelSerializer):
    # token = serializers.Field(source='my_token')

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'country_code', 'contact_no',
                  'created', 'modified', 'city', 'state', 'country')

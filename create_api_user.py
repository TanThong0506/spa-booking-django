#!/usr/bin/env python3
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spa_booking.settings')
import django

django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

def main():
    User = get_user_model()
    username = 'apitest'
    email = 'apitest@example.com'
    password = 'ChangeMe123!'

    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_active': True})
    if created:
        user.set_password(password)
        user.save()

    token, _ = Token.objects.get_or_create(user=user)

    print('User:', username, '(created=' + str(created) + ')')
    print('Password:', password)
    print('Token:', token.key)
    print('\nExample curl to test a protected endpoint:')
    print(f"curl -H 'Authorization: Token {token.key}' http://127.0.0.1:8000/api/services/")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error creating API user/token:', e, file=sys.stderr)
        raise

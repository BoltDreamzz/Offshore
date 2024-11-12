# userauths/backends.py

from django.contrib.auth.backends import BaseBackend
from .models import User

# User  = get_user_model()

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None  # Return None if the user does not exist

        if user.check_password(password):  # Check if the password is correct
            return user  # Return the user instance if authentication is successful

        return None  # Return None if authentication fails

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None  # Return None if the user does not exist
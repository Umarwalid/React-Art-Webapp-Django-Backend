import firebase_admin
from firebase_admin import auth
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class FirebaseAuthentication(BaseBackend):
    def authenticate(self, request, id_token=None):
        if not id_token:
            id_token = self.get_token_from_request(request)

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            user, created = User.objects.get_or_create(username=uid, defaults={'email': email})
            return user, None  
        except Exception as e:
            return None, None  
    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            return None
        elif len(parts) == 1:
            return None
        elif len(parts) > 2:
            return None

        return parts[1]

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate_header(self, request):
        return 'Bearer'

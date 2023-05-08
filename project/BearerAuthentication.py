from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def get_model_and_token(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
            return (token.user, token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

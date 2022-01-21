import datetime

import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import User
from .serializers import UserSerializer

jwt_key = settings.JWT_KEY

class TokenHandler:
  @staticmethod
  def token_encode(data:UserSerializer, exp_time:int):
    encoded_data = {'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=exp_time)}
    encoded_data.update(data)
    return encoded_data, jwt.encode(encoded_data, jwt_key, algorithm="HS256")

  @staticmethod
  def token_decode(auth_header:str=None):
    """
    Split value from Authorization header and decode them
    """
    jwt_token = auth_header.split()[1]
    try:
      decoded_token = jwt.decode(jwt_token, jwt_key, algorithms="HS256")
      return decoded_token
    except:
      return None

class UserAuthentication(BaseAuthentication):
  """
  Return user ID from request Authorization header
  """
  def authenticate(self, request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
      # the authorization header is empty
      raise exceptions.AuthenticationFailed('Auth header is empty')
    jwt_payload = TokenHandler.token_decode(auth_header)
    if not jwt_payload:
      # an error occured in jwt decoding process
      raise exceptions.AuthenticationFailed('JWT token expired/invalid')
    user_id_query = User.objects.get_or_create(uid=jwt_payload['uid'])
    return (user_id_query, None)

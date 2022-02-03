from django.conf import settings
from rest_framework import exceptions
from rest_framework.permissions import BasePermission

from .serializers import UserSerializer


class ServerPermission(BasePermission):
    """
    Implementation on server to server authentication, making sure that token provided in request header is the same as token in django settings
    """

    def has_permission(self, request, view):
        server_token_header = request.META.get("HTTP_SERVER_TOKEN")
        if not server_token_header:
            # Server-Token header is empty
            raise exceptions.PermissionDenied("Header is empty")

        prefix = server_token_header.split()[0]
        token_payload = server_token_header.split()[1]
        if prefix != "Token" or token_payload != settings.SERVER_TOKEN:
            # Server token header invalid
            raise exceptions.PermissionDenied("Token/Header invalid")

        return True

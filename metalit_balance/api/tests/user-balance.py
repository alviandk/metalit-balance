from django.urls import reverse
import json
import jwt
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User, UserBalance
from api.serializers import UserBalanceSerializer


class GetUserBalanceTestCase(APITestCase):
    def setUp(self):
        """
        Setup before the test run
        """
        self.url = reverse("get_user_balance")
        self.user = User.objects.create(name="user-test")
        self.user_balance = UserBalance.objects.create(uid=self.user, balance=0)
        self.auth_url = reverse("generate-token", kwargs={"user_id": self.user.uid})

    def test_get_user_balance_auth_success(self):
        """
        Test to make sure that get user balance API will work if authentication success
        """
        # Get data from db
        query = UserBalance.objects.all()
        user = User.objects.get(name=self.user.name)
        serializer = UserBalanceSerializer(query, many=True)

        # Simulate successful authentication
        auth_request = self.client.get(self.auth_url)
        jwt_token = auth_request.data["token"]

        header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
        request = self.client.get(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data[0], request.data["results"][0])

    def test_get_user_balance_auth_fail_no_header(self):
        """
        Test to make sure that user balance API will not work if no Authorization header is provided
        """
        # Simulate fail authentication
        request = self.client.get(self.url)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_balance_auth_fail_jwt_expired_or_invalid(self):
        """
        Test to make sure that get user balance API will not work if JWT token provided in Authorization header is invalid/expired
        """
        # Simulate fail authentication
        header = {"HTTP_AUTHORIZATION": "Token invalidtoken"}
        request = self.client.get(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_user_challenge(self):
        """
        Test to make user user balance api will not work with POST method
        """
        # Simulate successful authentication
        auth_request = self.client.get(self.auth_url)
        jwt_token = auth_request.data["token"]

        header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
        request = self.client.post(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_user_challenge(self):
        """
        Test to make user user balance api will not work with PUT method
        """
        # Simulate successful authentication
        auth_request = self.client.get(self.auth_url)
        jwt_token = auth_request.data["token"]

        header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
        request = self.client.put(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user_challenge(self):
        """
        Test to make user user balance api will not work with PATCH method
        """
        # Simulate successful authentication
        auth_request = self.client.get(self.auth_url)
        jwt_token = auth_request.data["token"]

        header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
        request = self.client.patch(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

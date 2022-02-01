from django.conf import settings
from django.urls import reverse
import json
import jwt
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User, UserBalance
from api.serializers import UserBalanceSerializer


class UserRecevieRewardTestCase(APITestCase):
    def setUp(self):
        """
        Setup before the test run
        """
        self.url = reverse("user_receive_reward")
        self.user = User.objects.create(name="user-test")
        self.user_balance = UserBalance.objects.create(uid=self.user, balance=0)

    # def test_get_user_receive_reward(self):
    #     """
    #     Test to make sure that user receive reward API will not work with GET
    #     """
    #     # Simulate successful server permission
    #     header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}
    #     request = self.client.get(self.url, **header)

    #     self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # def test_post_user_receive_reward_permission_success(self):
    #     """
    #     Test to make sure that user receive reward API will work with POST method if permission success
    #     """
    #     # Simulate successful server permission
    #     header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

    #     body = {
    #         "uid": self.user.uid,
    #         "account_number": self.user_balance.account_number,
    #         "amount": 50000,
    #     }
    #     request = self.client.post(self.url, body, **header)

    #     self.assertEqual(request.status_code, status.HTTP_200_OK)

    #     # Check balance added
    #     balance = UserBalance.objects.get(uid=self.user.uid).balance
    #     self.assertEqual(balance, 50000)

    def test_post_user_receive_reward_permission_failed(self):
        """
        Test to make sure that user receive reward API will not work if permission failed
        """
        # Simulate fail server permission
        header = {"HTTP_SERVER_TOKEN": f"Token failtoken"}

        body = {
            "uid": self.user.uid,
            "account_number": self.user_balance.account_number,
            "amount": 50000,
        }
        request = self.client.post(self.url, body, **header)

        print(request.data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    # def test_put_user_challenge(self):
    #     """
    #     Test to make user user balance api will not work with PUT method
    #     """
    #     # Simulate successful authentication
    #     auth_request = self.client.get(self.auth_url)
    #     jwt_token = auth_request.data["token"]

    #     header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
    #     request = self.client.put(self.url, **header)

    #     self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # def test_patch_user_challenge(self):
    #     """
    #     Test to make user user balance api will not work with PATCH method
    #     """
    #     # Simulate successful authentication
    #     auth_request = self.client.get(self.auth_url)
    #     jwt_token = auth_request.data["token"]

    #     header = {"HTTP_AUTHORIZATION": f"Token {jwt_token}"}
    #     request = self.client.patch(self.url, **header)

    #     self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

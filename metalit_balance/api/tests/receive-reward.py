from api.models import User, UserBalance
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserReceiveRewardTestCase(APITestCase):
    def setUp(self):
        """
        Setup before the test run
        """
        self.url = reverse("user_receive_reward")
        self.user = User.objects.create(name="user-test")
        self.user_balance = UserBalance.objects.create(uid=self.user, balance=0)

    def test_get_user_receive_reward(self):
        """
        Test to make sure that user receive reward API will not work with GET
        """
        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}
        request = self.client.get(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_user_receive_reward_permission_success(self):
        """
        Test to make sure that user receive reward API will work with POST method if permission success
        """
        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

        body = {
            "uid": self.user.uid,
            "account_number": self.user_balance.account_number,
            "amount": 50000,
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Check balance added
        balance = UserBalance.objects.get(uid=self.user.uid).balance
        self.assertEqual(balance, 50000)

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

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_user_receive_reward_body_incomplete(self):
        """
        Test to make sure that user receive reward API will not work with uncomplete body
        """
        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

        # Incomplete body
        body = {
            "uid": self.user.uid,
            "account_number": self.user_balance.account_number,
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_user_receive_reward_invalid_body(self):
        """
        Test to make sure that user receive reward API will not work with invalid body
        """
        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

        # Invalid body uid
        body = {
            "uid": f"{self.user.uid}a",
            "account_number": self.user_balance.account_number,
            "amount": "123",
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid body account number
        body = {
            "uid": self.user.uid,
            "account_number": f"{self.user_balance.account_number}a",
            "amount": "123",
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid amount (not int parseable)
        body = {
            "uid": self.user.uid,
            "account_number": self.user_balance.account_number,
            "amount": "123a",
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid amount (negative amount)
        body = {
            "uid": self.user.uid,
            "account_number": self.user_balance.account_number,
            "amount": -50000,
        }
        request = self.client.post(self.url, body, **header)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_user_receive_reward(self):
        """
        Test to make sure user receive reward API will not work with PUT method
        """

        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

        request = self.client.put(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user_receive_reward(self):
        """
        Test to make sure user receive reward API will not work with PATCH method
        """

        # Simulate successful server permission
        header = {"HTTP_SERVER_TOKEN": f"Token {settings.SERVER_TOKEN}"}

        request = self.client.patch(self.url, **header)

        self.assertEqual(request.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

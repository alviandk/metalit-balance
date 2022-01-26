from django.forms import ValidationError
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import UserAuthentication, TokenHandler
from .models import UserBalance, User, UserTransactionHistory
from .serializers import (
    UserBalanceSerializer,
    UserSerializer,
    UserTransactionHistorySerializer,
)

# Create your views here.


class TestingAddBalance(APIView):
    def get(self, request):
        UserBalance.add_balance("d79386797abe4641b5ec88f56ab90edf", 50000)
        return Response({"detail": "balance added 50000"}, status=status.HTTP_200_OK)


class TestingDeductBalance(APIView):
    def get(self, request):
        if UserBalance.deduct_balance("d79386797abe4641b5ec88f56ab90edf", 50000):
            return Response(
                {"detail": "balance deducted 50000"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "balance not enough"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserBalanceView(ListAPIView):
    """
    GET user balance from database
    """

    authentication_classes = [UserAuthentication]
    serializer_class = UserBalanceSerializer

    def get_queryset(self):
        """
        Override default queryset method on ListAPIView
        """

        # Get uid from authentication
        uid = self.request.user[0].uid

        query = UserBalance.objects.filter(uid=uid)

        obj = get_list_or_404(query)

        return obj


class UserTransactionHistoryView(ListAPIView):
    """
    GET user transaction history from database
    """

    authentication_classes = [UserAuthentication]
    serializer_class = UserTransactionHistorySerializer

    def get_queryset(self):
        """
        Override default queryset method on ListAPIView
        """
        # Get uid from authentication
        uid = self.request.user[0].uid

        query = UserTransactionHistory.objects.filter(uid=uid)

        obj = get_list_or_404(query)

        return obj


class UserTopUpView(APIView):
    """
    API to add balance to user
    """

    def post(self, request):
        try:
            uid = request.data["uid"]
            account_number = request.data["account_number"]
            amount = request.data["amount"]

            user_instance = User.objects.get(uid=uid)
            user_balance_instance = UserBalance.objects.get(
                uid=uid, account_number=account_number
            )

            with transaction.atomic():
                UserBalance.add_balance(uid, amount)

                instance = UserTransactionHistory(
                    uid=user_instance,
                    account_number=user_balance_instance,
                    amount=amount,
                    description=f"topup {amount}",
                )
                instance.save()

        except KeyError as e:
            return Response({"detail": "incomplete request body"})

        except ValidationError:
            return Response({"detail": "request body wrong"})

        return Response({"detail": "balance added"})


class UserRewardView(APIView):
    pass


class GenerateJWTMockup(APIView):
    """
    Mockup API to generate JWT token
    """

    def get(self, request, *args, **kwargs):
        # Mockup query
        query = User.objects.get(uid=kwargs.get("user_id"))
        serializer = UserSerializer(query, many=False)

        # JWT encode process
        encoded_data, token = TokenHandler.token_encode(serializer.data, 24)

        return Response(
            {"data_from_query": encoded_data, "token": token}, status=status.HTTP_200_OK
        )


class TestJWTResponse(APIView):
    """
    Mockup API to test JWT token generated
    """

    authentication_classes = [UserAuthentication]

    def get(self, request):
        # if authorization header is specified and jwt token is valid
        return Response({"message": "testing JWT success"})

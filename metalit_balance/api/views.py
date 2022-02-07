from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.forms import ValidationError
from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import TokenHandler, UserAuthentication
from .models import User, UserBalance, UserTransactionHistory
from .permissions import ServerPermission
from .serializers import (
    UserBalanceSerializer,
    UserSerializer,
    UserTransactionHistorySerializer,
)

# Create your views here.
# TODO: refactor code to make it cleaner

# TODO: revamp logic testing internal method
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

    permission_classes = [ServerPermission]

    def post(self, request):
        try:
            uid = request.data["uid"]
            account_number = request.data["account_number"]
            amount = request.data["amount"]
            trx_code = request.data["trx_code"]

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
                    trx_code=trx_code,
                )
                instance.save()

            serializer = UserTransactionHistorySerializer(instance)

            return Response({"detail": "balance added", "trx": serializer.data})

        except KeyError as e:
            return Response(
                {"detail": "incomplete request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except ObjectDoesNotExist:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError:
            return Response(
                {"detail": "trx-code must be unique"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserWithdrawView(APIView):
    """
    API to deduct balance from user
    """

    permission_classes = [ServerPermission]

    def post(self, request):
        try:
            uid = request.data["uid"]
            account_number = request.data["account_number"]
            amount = request.data["amount"]
            trx_code = request.data["trx_code"]

            user_instance = User.objects.get(uid=uid)
            user_balance_instance = UserBalance.objects.get(
                uid=uid, account_number=account_number
            )

            with transaction.atomic():
                UserBalance.deduct_balance(uid, amount)

                instance = UserTransactionHistory(
                    uid=user_instance,
                    account_number=user_balance_instance,
                    amount=amount,
                    description=f"withdraw {amount}",
                    trx_code=trx_code,
                )
                instance.save()

            serializer = UserTransactionHistorySerializer(instance)

            return Response({"detail": "balance withdrawed", "trx": serializer.data})

        except KeyError:
            return Response(
                {"detail": "incomplete request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except ObjectDoesNotExist:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError:
            return Response(
                {"detail": "trx-code must be unique"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserBalanceCreationView(APIView):
    """
    API to create record on user balance table
    """

    def post(self, request):
        serializer = UserBalanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReceiveRewardView(APIView):
    """
    API to add balance to user balance table when user receive reward
    """

    permission_classes = [ServerPermission]

    def post(self, request):
        try:
            uid = request.data["uid"]
            account_number = request.data["account_number"]
            amount = request.data["amount"]
            trx_code = request.data["trx_code"]

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
                    trx_code=trx_code,
                )
                instance.save()

            serializer = UserTransactionHistorySerializer(instance)

            return Response({"detail": "balance added", "trx": serializer.data})

        except KeyError:
            return Response(
                {"detail": "incomplete request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except ObjectDoesNotExist:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError:
            return Response(
                {"detail": "trx-code must be unique"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserBuyProductView(APIView):
    """
    API to deduct balance from user balance table when user buy product with their balance
    """

    permission_classes = [ServerPermission]

    def post(self, request):
        try:
            uid = request.data["uid"]
            account_number = request.data["account_number"]
            amount = request.data["amount"]
            trx_code = request.data["trx_code"]

            user_instance = User.objects.get(uid=uid)
            user_balance_instance = UserBalance.objects.get(
                uid=uid, account_number=account_number
            )

            with transaction.atomic():
                UserBalance.deduct_balance(uid, amount)

                instance = UserTransactionHistory(
                    uid=user_instance,
                    account_number=user_balance_instance,
                    amount=amount,
                    description=f"buy product for {amount}",
                    trx_code=trx_code,
                )
                instance.save()

            serializer = UserTransactionHistorySerializer(instance)

            return Response({"detail": "balance withdrawed", "trx": serializer.data})

        except KeyError:
            return Response(
                {"detail": "incomplete request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except ObjectDoesNotExist:
            return Response(
                {"detail": "request body invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError:
            return Response(
                {"detail": "trx-code must be unique"},
                status=status.HTTP_400_BAD_REQUEST,
            )


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

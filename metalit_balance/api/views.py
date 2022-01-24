from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import UserAuthentication, TokenHandler
from .models import UserBalance, User
from .serializers import UserBalanceSerializer, UserSerializer

# Create your views here.

class TestingAddBalance(APIView):
  def get(self, request):
    UserBalance.add_balance("d79386797abe4641b5ec88f56ab90edf", 50000)
    return Response({"detail": "balance added 50000"}, status=status.HTTP_200_OK)

class TestingDeductBalance(APIView):
  def get(self, request):
    if UserBalance.deduct_balance("d79386797abe4641b5ec88f56ab90edf", 50000):
      return Response({"detail": "balance deducted 50000"}, status=status.HTTP_200_OK)
    else:
      return Response({"detail": "balance not enough"}, status=status.HTTP_400_BAD_REQUEST)\

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

    query = UserBalance.objects.filter(
      uid = uid
    )

    obj = get_list_or_404(query)

    return obj


class UserBalanceHistoryView(ListAPIView):
  pass

class UserRewardView(APIView):
  pass

class GenerateJWTMockup(APIView):
  """
  Mockup API to generate JWT token
  """
  def get(self, request, *args, **kwargs):
    # Mockup query
    query = User.objects.get(uid=kwargs.get('user_id'))
    serializer = UserSerializer(query, many=False)

    # JWT encode process
    encoded_data, token = TokenHandler.token_encode(serializer.data, 24)

    return Response({"data_from_query": encoded_data, "token": token}, status=status.HTTP_200_OK)

class TestJWTResponse(APIView):
  """
  Mockup API to test JWT token generated
  """
  authentication_classes = [UserAuthentication]
  def get(self, request):
    # if authorization header is specified and jwt token is valid
    return Response({"message": "testing JWT success"})
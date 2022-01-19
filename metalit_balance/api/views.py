from django.shortcuts import render
from .models import UserBalance
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
      return Response({"detail": "balance not enough"}, status=status.HTTP_400_BAD_REQUEST)
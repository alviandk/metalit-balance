from django.shortcuts import render
from .models import UserBalance
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class Testing(APIView):
  def get(self, request):
    UserBalance.add_balance("d79386797abe4641b5ec88f56ab90edf", 50000)
    return Response({"detail": "testing add method"}, status.HTTP_200_OK)
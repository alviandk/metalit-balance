from dataclasses import field
from rest_framework import serializers
from .models import User, UserBalance, UserTransactionHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = "__all__"


class UserTransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransactionHistory
        fields = "__all__"

from django.urls import path

from django.conf import settings
from .views import TestingAddBalance, TestingDeductBalance, UserBalanceView, GenerateJWTMockup, TestJWTResponse, UserTopUpView, UserTransactionHistoryView

urlpatterns = [
  path('user-balance/get', UserBalanceView.as_view()),
  path('user-transaction-history/get', UserTransactionHistoryView.as_view()),
  path('user/topup', UserTopUpView.as_view()),
]

"""
Additional API for dev mode
"""
if settings.DEV_MODE:
  urlpatterns += [
    # Endpoint to test internal method
    path('add-balance', TestingAddBalance.as_view()),
    path('deduct-balance', TestingDeductBalance.as_view()),
    path('auth/generate-token/<str:user_id>', GenerateJWTMockup.as_view()),
    path('auth/test-token', TestJWTResponse.as_view()),
  ]
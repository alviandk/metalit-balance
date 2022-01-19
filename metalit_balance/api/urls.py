from django.urls import path

from django.conf import settings
from .views import TestingAddBalance, TestingDeductBalance

urlpatterns = [

]

"""
Additional API for dev mode
"""
if settings.DEV_MODE:
  urlpatterns += [
    # Endpoint to test internal method
    path('add-balance', TestingAddBalance.as_view()),
    path('deduct-balance', TestingDeductBalance.as_view()),
  ]
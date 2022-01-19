from django.urls import path

from .views import Testing

urlpatterns = [
  path('add-balance', Testing.as_view())
]
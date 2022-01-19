from statistics import mode
import uuid
from django.db import models

# Create your models here.
class User(models.Model):
  """
  Model for user table in database (mockup)
  """
  class Meta:
    ordering = ['created_at']

  uid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
  name = models.CharField(max_length=255, null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)

  def __str__(self):
    return f"{self.name}"

class UserBalance(models.Model):
  """
  Model for user_balance table in database
  """
  # class Meta:
  #   ordering = ['id']

  uid = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    to_field = "uid",
    db_column = "uid"
  )
  balance = models.BigIntegerField(null=False, default=0)
  action = models.CharField(max_length=255, blank=True, default=None)

  @staticmethod
  def add_balance(uid, amount):
    user_balance = UserBalance.objects.get(uid=uid)
    user_balance.balance += amount
    user_balance.save()

  @staticmethod
  def deduct_balance(uid, balance):
    pass
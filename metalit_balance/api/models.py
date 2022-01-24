from statistics import mode
import uuid
from django.db import models

# Create your models here.
class User(models.Model):
  """
  Model for user table in database (mockup)
  """
  class Meta:
    ordering = ['-created_at']

  uid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
  name = models.CharField(max_length=255, null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)

  def __str__(self):
    return f"{self.name}"

class UserBalance(models.Model):
  """
  Model for user_balance table in database
  """
  class Meta:
    ordering = ['-id']
    constraints = [
      models.UniqueConstraint(fields=['uid', 'account_number'], name='unique uid acc_number')
    ]

  uid = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    to_field = "uid",
    db_column = "uid"
  )
  account_number = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
  balance = models.BigIntegerField(null=False, default=0)
  action = models.CharField(max_length=255, blank=True, default=None)

  def __str__(self):
    return f"{self.uid}"

  @staticmethod   
  def add_balance(uid, amount):
    """
    Internal method to add balance based on uid
    """
    user_balance = UserBalance.objects.get(uid=uid)
    user_balance.balance += amount
    user_balance.save()

  @staticmethod
  def deduct_balance(uid, amount):
    """
    Internal method to deduct balance based on uid
    """
    user_balance = UserBalance.objects.get(uid=uid)
    if(user_balance.balance<amount):
      #trying to deduct amount that is greater than the balance
      return False
    else:
      user_balance.balance -= amount
      user_balance.save()
      return True

class UserHistory(models.Model):
  """
  Model for user_history table in database
  """
  class Meta:
    ordering = ['-created_at']
    constraints = [
      models.UniqueConstraint(fields=['uid', 'account_number', 'transaction_id'], name='unique uid acc_number trans_id')
    ]

  uid = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    to_field = "uid",
    db_column = "uid"
  )
  account_number = models.ForeignKey(
    UserBalance,
    on_delete = models.CASCADE,
    to_field = "account_number",
    db_column = "account_number"
  )
  transaction_id = models.CharField(max_length=255, editable=False, default=uuid.uuid4, unique=True)
  amount = models.BigIntegerField(null=False)
  description = models.CharField(max_length=255, blank=True, default="")
  created_at = models.DateTimeField(auto_now_add=True, null=False)
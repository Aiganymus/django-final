from django.db import models

from users.models import MainUser
from utils.constants import ACCOUNT_TYPES, ORDINARY, OPERATION_TYPES


class AccountManager(models.Manager):
    def check_balance(self, instance, amount):
        print(instance.balance, amount, instance.min_amount)
        if instance.balance < amount or instance.balance - amount < instance.min_amount:
            return False
        return True


class Account(models.Model):
    number = models.IntegerField(unique=True, primary_key=True)
    balance = models.PositiveIntegerField(default=0)
    min_amount = models.PositiveIntegerField(default=0)
    opened_date = models.DateTimeField(auto_now_add=True)
    account_type = models.PositiveIntegerField(choices=ACCOUNT_TYPES, default=ORDINARY)
    monthly_fee = models.PositiveIntegerField(default=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='account')

    accounts = AccountManager()
    objects = models.Manager()

    def check_balance(self, amount):
        return self.balance > amount and self.balance - amount > self.min_amount


class Transaction(models.Model):
    amount = models.PositiveIntegerField()
    operation_type = models.PositiveIntegerField(choices=OPERATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='transactions')

    def __str__(self):
        return f'Transaction: {self.amount} {self.operation_type} {self.created_at} {self.account.owner.username}'

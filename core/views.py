from django.db.models import F
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from core.models import Account, Transaction
from core.serializers import AccountSerializer, TransactionSerializer
from users.serializers import UserSerializer
from utils.constants import DEPOSIT, WITHDRAW, TRANSFER
from utils.permissions import OwnerPermission
import logging

logger = logging.getLogger(__name__)


class AccountViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'number'
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated, OwnerPermission)
    serializer_class = AccountSerializer

    @action(methods=['POST'], detail=False)
    def deposit(self, request):
        account = request.user.account
        amount = int(request.data.get('amount'))
        account.update(balance=F('balance') + amount)
        trans = Transaction(amount=amount, account=account.get(), operation_type=DEPOSIT)
        trans.save()
        logger.info(trans)
        return Response('ok')

    @action(methods=['POST'], detail=False)
    def withdraw(self, request):
        account = request.user.account
        instance = account.get()
        amount = int(request.data.get('amount'))
        if not Account.accounts.check_balance(instance, amount):
            logger.error('Could not make transaction: Not enough balance!')
            return Response('Not enough money on balance.', status=status.HTTP_406_NOT_ACCEPTABLE)
        account.update(balance=F('balance') - amount)
        trans = Transaction(amount=amount, account=instance, operation_type=WITHDRAW)
        trans.save()
        logger.info(trans)
        return Response('ok')

    @action(methods=['POST'], detail=False)
    def transfer(self, request):
        account = request.user.account
        instance = account.get()
        amount = int(request.data.get('amount'))
        user_id = int(request.data.get('user'))
        transfer_to = Account.objects.get(owner__id=user_id)
        if not Account.accounts.check_balance(instance, amount):
            logger.error('Could not make transaction: Not enough balance!')
            return Response('Not enough money on balance.', status=status.HTTP_406_NOT_ACCEPTABLE)
        with transaction.atomic():
            account.update(balance=F('balance') - amount)
            transfer_to.balance += amount
            transfer_to.save()
        trans = Transaction(amount=amount, account=instance, operation_type=TRANSFER)
        trans.save()
        logger.info(trans)
        return Response('ok')

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def transactions(self, request):
        transactions = Transaction.objects.filter(account=request.user.account.get())
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

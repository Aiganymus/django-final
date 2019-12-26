from rest_framework import serializers

from core.models import Account, Transaction
from users.serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Account
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.min_amount = validated_data.get('min_amount', instance.min_amount)
        account_type = int(validated_data.get('account_type'))
        if account_type is not None:
            if account_type == 0:
                instance.monthly_fee = 100
            elif account_type == 1:
                instance.monthly_fee = 150
            else:
                instance.monthly_fee = 200
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField(read_only=True)
    account = AccountSerializer(write_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

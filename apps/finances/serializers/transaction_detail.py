# apps/finances/serializers/transaction_detail.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.finances.models import TransactionDetail, Account


class TransactionDetailSerializer(ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = ['account', 'debit_amount', 'credit_amount']

    def validate(self, data):
        """차변/대변 검증"""
        debit_amount = data.get('debit_amount', 0)
        credit_amount = data.get('credit_amount', 0)

        # 차변과 대변 중 하나만 0이 아니어야 함
        if debit_amount > 0 and credit_amount > 0:
            raise serializers.ValidationError("차변과 대변 중 하나만 입력해야 합니다.")

        if debit_amount == 0 and credit_amount == 0:
            raise serializers.ValidationError("차변 또는 대변 금액을 입력해야 합니다.")

        return data

    def validate_account(self, value):
        """계정과목 검증"""
        if not isinstance(value, Account):
            raise serializers.ValidationError("유효한 계정과목을 선택해야 합니다.")
        return value
# apps/finances/serializers/journal_entry.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db import transaction
from apps.finances.models import JournalEntry, TransactionDetail
from .transaction_detail import TransactionDetailSerializer

class JournalEntryCreateSerializer(ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = ['book', 'entry_date', 'description', 'transaction_details']

    def validate_book(self, value):
        """장부 소유권 검증"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if value.user_id != request.user.id:
                raise serializers.ValidationError("본인 소유의 장부만 사용할 수 있습니다.")
        return value

    def validate_transaction_details(self, value):
        """대차평형 검증"""
        if len(value) < 2:
            raise serializers.ValidationError("최소 2개의 거래 상세가 필요합니다.")

        total_debit = sum(detail.get('debit_amount', 0) for detail in value)
        total_credit = sum(detail.get('credit_amount', 0) for detail in value)

        if total_debit != total_credit:
            raise serializers.ValidationError(
                f"차변 합계({total_debit})와 대변 합계({total_credit})가 일치하지 않습니다."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        """JournalEntry와 TransactionDetail 동시 생성"""
        transaction_details_data = validated_data.pop('transaction_details')

        # JournalEntry 생성
        journal_entry = JournalEntry.objects.create(**validated_data)

        # TransactionDetail 생성
        for detail_data in transaction_details_data:
            detail_data['journal_entry'] = journal_entry
            TransactionDetail.objects.create(**detail_data)

        return journal_entry

class JournalEntryDetailSerializer(ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['id', 'book', 'entry_date', 'description', 'reference_id',
                  'created_at', 'transaction_details']
        read_only_fields = ['id', 'created_at', 'reference_id']

class JournalEntryListSerializer(ModelSerializer):
    total_debit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_credit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['id', 'book', 'entry_date', 'description', 'total_debit', 'total_credit']
        read_only_fields = ['id', 'total_debit', 'total_credit']
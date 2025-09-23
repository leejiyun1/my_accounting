# apps/finances/models/transaction_detail.py

from django.db import models
from .journal_entry import JournalEntry
from .account import Account


class TransactionDetail(models.Model):
    """
    분개 상세 모델 (복식부기의 차변/대변)
    """

    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='transaction_details',
        help_text="분개"
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        help_text="계정과목"
    )

    debit_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="차변 금액"
    )

    credit_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="대변 금액"
    )

    class Meta:
        db_table = 'transaction_details'
        verbose_name = '분개 상세'
        verbose_name_plural = '분개 상세들'
        indexes = [
            models.Index(fields=['journal_entry']),
            models.Index(fields=['account']),
        ]

    def __str__(self):
        if self.debit_amount > 0:
            return f"{self.account.account_name} 차변 {self.debit_amount:,}"
        else:
            return f"{self.account.account_name} 대변 {self.credit_amount:,}"

    def clean(self):
        """validation: 차변이나 대변 중 하나만 0이 아니어야 함"""
        from django.core.exceptions import ValidationError

        if self.debit_amount > 0 and self.credit_amount > 0:
            raise ValidationError("차변과 대변 중 하나만 입력해야 합니다.")

        if self.debit_amount == 0 and self.credit_amount == 0:
            raise ValidationError("차변 또는 대변 금액을 입력해야 합니다.")

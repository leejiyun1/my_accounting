# apps/finances/models/journal_entry.py

from django.db import models
from django.utils import timezone


class JournalEntry(models.Model):
    """
    분개장 모델 (거래 단위)
    """

    book = models.ForeignKey(
    'Book',
    on_delete=models.CASCADE,
    help_text="소속 장부"
)

    entry_date = models.DateField(
        help_text="거래 일자"
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="거래 설명"
    )

    reference_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="참조 ID (AI 파싱 시 원본 데이터 참조용)"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="생성 시간"
    )

    class Meta:
        db_table = 'journal_entries'
        verbose_name = '분개'
        verbose_name_plural = '분개들'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['entry_date']),
        ]

    def __str__(self):
        return f"{self.entry_date} - {self.description}"

    @property
    def total_debit(self):
        """총 차변 금액"""
        return sum(detail.debit_amount for detail in self.transaction_details.all())

    @property
    def total_credit(self):
        """총 대변 금액"""
        return sum(detail.credit_amount for detail in self.transaction_details.all())

    @property
    def is_balanced(self):
        """차변 = 대변 균형 확인"""
        return self.total_debit == self.total_credit

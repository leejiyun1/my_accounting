from django.db import models
from django.utils import timezone

class Book(models.Model):
    """
    장부 모델
    """

    BOOK_TYPE_CHOICES = [
        ('personal', '개인장부'),
        ('business', '사업장부')
    ]

    user_id = models.BigIntegerField(
        help_text="사용자 ID (외래키 제약 없이 참조)"
    )

    book_type = models.CharField(
        max_length=20,
        choices=BOOK_TYPE_CHOICES,
        help_text="장부 유형"
    )

    name = models.CharField(
        max_length=100,
        help_text="장부 이름"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="생성 일시"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="수정 일시"
    )
    class Meta:
        db_table = 'books'
        verbose_name = '장부'
        verbose_name_plural = '장부들'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['user_id', 'book_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_book_type_display()})"
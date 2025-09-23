# apps/schedules/models/schedule_category.py

from django.db import models
from django.utils import timezone


class ScheduleCategory(models.Model):
    """
    일정 카테고리 모델
    """

    user_id = models.BigIntegerField(
        help_text="사용자 ID (외래키 제약 없이 참조)"
    )

    name = models.CharField(
        max_length=50,
        help_text="카테고리 이름"
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="색상 코드 (hex)"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="생성 시간"
    )

    class Meta:
        db_table = 'schedule_categories'
        verbose_name = '일정 카테고리'
        verbose_name_plural = '일정 카테고리들'
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"User {self.user_id} - {self.name}"
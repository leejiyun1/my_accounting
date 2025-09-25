from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.schedules.models import Schedule
from apps.schedules.serializers.schedule import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    스케줄을 관리하는 뷰셋입니다.
    """
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """사용자 별로 스케줄을 필터링합니다."""
        return Schedule.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        """새 스케줄 생성 시 현재 사용자를 설정합니다."""
        serializer.save(user_id=self.request.user.id)
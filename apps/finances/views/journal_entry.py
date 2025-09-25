# apps/finances/views/journal_entry.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.finances.serializers.journal_entry import JournalEntryCreateSerializer
from apps.finances.services.journal_entry import JournalEntryService
from apps.finances.models import JournalEntry
from apps.finances.serializers.journal_entry import JournalEntryListSerializer, JournalEntryDetailSerializer

class JournalEntryCreateView(APIView):
    """
    거래 생성 API
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JournalEntryCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        journal_entry = serializer.save()
        transaction_summary = JournalEntryService.create_transaction_summary(journal_entry)
        return Response({
            "success": True,
            "message": "거래가 성공적으로 기록되었습니다",
            "data": {
                "id": journal_entry.id,
                "book_name": journal_entry.book.name,
                "description": journal_entry.description,
                "amount": journal_entry.total_debit,
                "transaction_summary": transaction_summary
            }
        }, status=status.HTTP_201_CREATED)


class JournalEntryListView(APIView):
    """
    거래 목록 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 거래 목록 조회 (장부별 필터링)
        book_id = request.query_params.get('book')
        queryset = JournalEntry.objects.filter(book__user_id=request.user.id)

        if book_id:
            queryset = queryset.filter(book_id=book_id)

        # 날짜 역순 정렬
        queryset = queryset.order_by('-entry_date', '-created_at')

        serializer = JournalEntryListSerializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

class JournalEntryDetailView(APIView):
    """
    거래 상세 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            journal_entry = JournalEntry.objects.get(
                pk=pk,
                book__user_id=request.user.id
            )
        except JournalEntry.DoesNotExist:
            return Response(
                {"error": "거래를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JournalEntryDetailSerializer(journal_entry)
        return Response({
            "success": True,
            "data": serializer.data
        })
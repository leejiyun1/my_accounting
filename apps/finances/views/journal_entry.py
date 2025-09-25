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
    거래 상세 조회/수정/삭제 API
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user_id):
        """공통 객체 조회 메서드"""
        try:
            return JournalEntry.objects.get(pk=pk, book__user_id=user_id)
        except JournalEntry.DoesNotExist:
            return None

    def get(self, request, pk):
        journal_entry = self.get_object(pk, request.user.id)
        if not journal_entry:
            return Response(
                {"error": "거래를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JournalEntryDetailSerializer(journal_entry)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def put(self, request, pk):
        """거래 수정"""
        journal_entry = self.get_object(pk, request.user.id)
        if not journal_entry:
            return Response(
                {"error": "거래를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JournalEntryCreateSerializer(
            journal_entry,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 기존 TransactionDetail 삭제 후 새로 생성
        journal_entry.transaction_details.all().delete()
        updated_entry = serializer.save()

        return Response({
            "success": True,
            "message": "거래가 성공적으로 수정되었습니다.",
            "data": {"id": updated_entry.id}
        })

    def delete(self, request, pk):
        """거래 삭제"""
        journal_entry = self.get_object(pk, request.user.id)
        if not journal_entry:
            return Response(
                {"error": "거래를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        journal_entry.delete()
        return Response({
            "success": True,
            "message": "거래가 성공적으로 삭제되었습니다."
        }, status=status.HTTP_204_NO_CONTENT)
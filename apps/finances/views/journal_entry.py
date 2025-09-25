# apps/finances/views/journal_entry.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.finances.serializers.journal_entry import JournalEntryCreateSerializer
from apps.finances.services.journal_entry import JournalEntryService

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
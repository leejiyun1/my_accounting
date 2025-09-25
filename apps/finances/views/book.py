from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.finances.models import Book
from apps.finances.serializers.book import BookCreateSerializer

class BookCreateView(APIView):
    """
    사용자 장부 생성 API
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_type = serializer.validated_data['book_type']
        name = serializer.validated_data['name']

        # 중복 체크 (같은 유형 장부가 이미 있는지)
        if Book.objects.filter(user_id=request.user.id, book_type=book_type).exists():
            return Response(
                {"error": f"{book_type} 장부가 이미 존재합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 장부 생성
        book = Book.objects.create(
            user_id=request.user.id,
            book_type=book_type,
            name=name
        )

        return Response(
            {
                "id": book.id,
                "book_type": book.book_type,
                "name": book.name,
                "created_at": book.created_at
            },
            status=status.HTTP_201_CREATED
        )
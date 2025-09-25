from rest_framework import serializers

class BookCreateSerializer(serializers.Serializer):
    book_type = serializers.ChoiceField(
        choices=[('personal', '개인장부'), ('business', '사업장부')],
        help_text="장부 유형 선택"
    )

    name = serializers.CharField(
        max_length=100,
        help_text="장부 이름"
    )

    def validate_book_type(self, value):
        if value not in ['personal', 'business']:
            raise serializers.ValidationError("유효하지 않은 장부 유형입니다.")
        return value
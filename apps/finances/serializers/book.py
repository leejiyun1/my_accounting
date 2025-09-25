from rest_framework import serializers


class BookCreateSerializer(serializers.Serializer):
    booktype = serializers.ChoiceField(
        choices=[('personal', '개인'), ('business', '사업자')],
        help_text="장부 유형 선택 (personal: 개인, business: 사업자)"
    )

    def validate_booktype(self, value):
        if value not in ['personal', 'business']:
            raise serializers.ValidationError("Invalid book type. Choose 'personal' or 'business'.")
        return value
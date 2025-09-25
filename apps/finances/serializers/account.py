from rest_framework.serializers import ModelSerializer
from apps.finances.models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_code', 'account_name', 'account_type', 'book_type', 'is_active']
        read_only_fields = ['id']
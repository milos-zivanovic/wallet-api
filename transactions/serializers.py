from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    type_sign = serializers.ReadOnlyField()
    full_category_str = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_type",
            "type_sign",
            "category",
            "full_category_str",
            "title",
            "description",
            "amount",
            "is_agency_related",
            "is_fixed",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

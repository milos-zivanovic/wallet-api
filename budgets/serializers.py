from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    total_spent = serializers.ReadOnlyField()
    percentage_spent = serializers.ReadOnlyField()
    category_name = serializers.ReadOnlyField(source="category.name")
    category_group_name = serializers.ReadOnlyField(source="category.category_group.name")

    class Meta:
        model = Budget
        fields = [
            "id",
            "category",
            "category_name",
            "category_group_name",
            "start_date",
            "end_date",
            "amount",
            "description",
            "total_spent",
            "percentage_spent",
        ]
        read_only_fields = ["id", "total_spent", "percentage_spent"]

from datetime import date
from decimal import Decimal
from .models import Budget

def get_active_budgets():
    today = date.today()
    active_budgets = Budget.objects.filter(
        start_date__lte=today, end_date__gte=today
    ).order_by("category__category_group_id", "category_id")

    total_amount = active_budgets.aggregate(total=models.Sum("amount"))["total"] or 0
    total_spent = sum(b.total_spent for b in active_budgets)
    # sort by percentage spent descending
    active_budgets = sorted(active_budgets, key=lambda b: b.percentage_spent, reverse=True)
    percentage_spent = (total_spent / total_amount * 100) if total_amount > 0 else 0
    return {
        "active_budgets": active_budgets,
        "total_amount": total_amount,
        "total_spent": total_spent,
        "percentage_spent": percentage_spent,
    }

def get_historical_budgets():
    today = date.today()
    return Budget.objects.exclude(
        start_date__lte=today, end_date__gte=today
    ).order_by("-start_date", "category__category_group_id", "category_id")

from datetime import timedelta
from django.db.models import Sum, Case, When, F, DecimalField
from django.db.models.functions import TruncDate


def calculate_totals(queryset):
    total_income = queryset.filter(transaction_type="income").aggregate(Sum("amount"))["amount__sum"] or 0
    total_expense = queryset.filter(transaction_type="expense").aggregate(Sum("amount"))["amount__sum"] or 0
    balance = total_income - total_expense
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }

def calculate_balance_by_day(queryset, from_date, to_date):
    # TODO: IMPLEMENT LATER BASED ON FRONTEND AND CHARTS
    return
    # daily_data = (
    #     queryset
    #     .filter(created_at__date__range=(from_date, to_date))
    #     .annotate(day=TruncDate("created_at"))
    #     .values("day")
    #     .annotate(
    #         net_amount=Sum(
    #             Case(
    #                 When(transaction_type="income", then=F("amount")),
    #                 When(transaction_type="expense", then=-F("amount")),
    #                 output_field=DecimalField(),
    #             )
    #         )
    #     )
    #     .order_by("day")
    # )
    #
    # daily_map = {row["day"]: row["net_amount"] for row in daily_data}
    #
    # result = {}
    # running_balance = 0
    # current = from_date
    # while current <= to_date:
    #     running_balance += daily_map.get(current, 0)
    #     result[current.strftime("%Y-%m-%d")] = running_balance
    #     current += timedelta(days=1)
    # return result


def category_expense_breakdown(queryset, category_group=None):
    # TODO: IMPLEMENT LATER BASED ON FRONTEND AND CHARTS
    return
    # if category_group:
    #     tmp_grouped_data = (
    #         queryset.filter(transaction_type="expense", category__category_group_id=category_group)
    #         .values("category__name")
    #         .annotate(total_amount=Sum("amount"))
    #     )
    #     grouped_data = {}
    #     for row in tmp_grouped_data:
    #         grouped_data[row["category__name"]] = grouped_data.get(row["category__name"], 0) + row["total_amount"]
    # else:
    #     tmp_grouped_data = (
    #         queryset.filter(transaction_type="expense")
    #         .values("category__category_group__name")
    #         .annotate(total_amount=Sum("amount"))
    #     )
    #     grouped_data = {}
    #     for row in tmp_grouped_data:
    #         grouped_data[row["category__category_group__name"]] = grouped_data.get(row["category__category_group__name"], 0) + row["total_amount"]
    #
    # # sort descending
    # return dict(sorted(grouped_data.items(), key=lambda x: x[1], reverse=True))

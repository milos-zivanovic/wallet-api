from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter
from .services import calculate_totals, calculate_balance_by_day, category_expense_breakdown


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(is_deleted=False, user=self.request.user).select_related(
            "category", "category__category_group"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=["get"])
    def overview(self, request):
        base_qs = self.get_queryset()
        filterset = TransactionFilter(request.GET, queryset=base_qs)
        qs = filterset.qs
        today = timezone.now()

        # Get filters
        first_transaction = base_qs.order_by("created_at").first()
        from_date = (first_transaction.created_at - timedelta(days=1)).date() if first_transaction else today.date()
        to_date = today.date()
        if request.GET.get("from_date"):
            from_date = datetime.strptime(request.GET["from_date"], "%Y-%m-%d").date()
        if request.GET.get("to_date"):
            to_date = datetime.strptime(request.GET["to_date"], "%Y-%m-%d").date()
        show = request.GET.get("show", "table").lower()

        # Calculate totals and prepare response object
        totals = calculate_totals(qs)
        response_data = {
            "show": show,
            "from_date": from_date.strftime("%Y-%m-%d"),
            "to_date": to_date.strftime("%Y-%m-%d"),
            "current_date": today.strftime("%Y-%m-%d"),
            "days_diff": (to_date - from_date).days + 1,
            "filters": request.GET,
            **totals
        }

        # TABLE mode
        if show == "table":
            page_number = request.GET.get("page", 1)
            paginator = Paginator(qs, 50)
            page_obj = paginator.get_page(page_number)
            serializer = self.get_serializer(page_obj.object_list, many=True)
            response_data["results"] = serializer.data
            response_data["pagination"] = {
                "page": page_obj.number,
                "pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "total_items": paginator.count
            }
            return Response(response_data)

        # CHART mode
        elif show == "chart":
            # TODO: IMPLEMENT LATER BASED ON FRONTEND AND CHARTS
            # category_group = request.GET.get("category_group")
            # response_data["category_chart"] = category_expense_breakdown(qs, category_group=category_group)
            # response_data["balance_by_day"] = calculate_balance_by_day(qs, from_date, to_date)
            # return Response(response_data)
            return Response({"detail": "Not implemented."}, status=400)

        else:
            return Response({"detail": "Invalid show parameter."}, status=400)


    @action(detail=False, methods=["get"])
    def title_suggestions(self, request):
        title = request.GET.get("title")
        if not title:
            return Response([])

        suggestions = self.get_queryset().filter(title__icontains=title)
        if datetime.now().month != 12:
            suggestions = suggestions.exclude(category_id=18)

        suggestions = suggestions.values(
            "title", "transaction_type", "category", "is_agency_related", "is_fixed"
        ).distinct()

        return Response([
            {
                "label": s["title"],
                "value": s["title"],
                "transaction_type": s["transaction_type"],
                "category": s["category"],
                "is_agency_related": s["is_agency_related"],
                "is_fixed": s["is_fixed"]
            } for s in suggestions
        ])

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Budget
from .serializers import BudgetSerializer
from .services import get_active_budgets, get_historical_budgets

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    @action(detail=False, methods=["get"])
    def overview(self, request):
        """
        Returns active budgets + historical budgets with totals.
        """
        active_data = get_active_budgets()
        historical_budgets = get_historical_budgets()
        serializer_active = self.get_serializer(active_data["active_budgets"], many=True)
        serializer_historical = self.get_serializer(historical_budgets, many=True)

        return Response({
            "active_budgets": serializer_active.data,
            "total_amount": active_data["total_amount"],
            "total_spent": active_data["total_spent"],
            "percentage_spent": active_data["percentage_spent"],
            "historical_budgets": serializer_historical.data,
        })

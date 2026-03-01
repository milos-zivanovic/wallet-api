from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet


app_name = 'budgets'
router = DefaultRouter()
router.register('', BudgetViewSet, basename="budget")

urlpatterns = router.urls

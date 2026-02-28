from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'transactions'
router = DefaultRouter()
# router.register('snippets', SnippetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

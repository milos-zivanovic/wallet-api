from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'categories'
router = DefaultRouter()
# router.register('snippets', SnippetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

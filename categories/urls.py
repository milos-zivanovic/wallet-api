from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'categories'
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

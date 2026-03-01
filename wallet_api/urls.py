"""
URL configuration for wallet_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def project_root(request):
    return Response({app: request.build_absolute_uri(f'/{app}/') for app in settings.CUSTOM_APPS})


urlpatterns = [
    path('', project_root),
    path('api-auth/', include('rest_framework.urls')),
    path('transactions/', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('budgets/', include('budgets.urls')),
]

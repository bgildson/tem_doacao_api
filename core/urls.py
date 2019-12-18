"""tem_doacao_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from categories.viewsets import CategoriesViewSet
from donations.viewsets import DonationsViewSet, DonationsImagesViewSet
from favorites.viewsets import FavoritesViewSet
from users.views import SignInUpView

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('donations', DonationsViewSet, basename='donations')
router.register('donations-images', DonationsImagesViewSet, basename='donations-images')
router.register('favorites', FavoritesViewSet, basename='favorites')

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Detailed Documentation for API Consumption.",
      contact=openapi.Contact(email="temdoacao@gmail.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls), name='api'),
    path('api/auth/sign-in-up/', SignInUpView.as_view(), name='sign_in_up'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

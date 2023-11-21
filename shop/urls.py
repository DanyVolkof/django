from django.contrib import admin
from django.urls import path
from shop.views import OrganizationListView, ShopView, shops_file, MyTokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated
from shop import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions


yasg_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version = "v1",
        description = "Descriiption",
        terms_of_service = "https://www.google.com/policies/terms/",
        contact = openapi.Contact(email="contact@snippets.local"),
        license = openapi.License(name="BSD Licence"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', views.shops_file),
    path('', views.ShopView),
    path('api/organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('api/organizations/<int:id>/shops_file/', views.shops_file, name='get-shops-file'),
    path('api/shops/<int:id>/', views.ShopView, name='shop-view'),
    path('api/v1/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('docs/', TemplateView.as_view(template_name='documentation.html', extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
    path('swagger<format>/', yasg_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', yasg_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', yasg_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


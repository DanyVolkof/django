from django.contrib import admin
from django.urls import path
from shop.views import OrganizationListView, ShopView, shops_file
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from rest_framework import routers
from rest_framework import permissions
from shop import views
from django.views.generic import TemplateView



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
    path('', views.OrganizationListView),
    path('', views.shops_file),
    path('', views.ShopView),
    path('api/organizations/', views.OrganizationListView, name='organizations-list'),
    path('api/organizations/<int:id>/shops_file/', views.shops_file, name='get-shops-file'),
    path('api/shops/<int:id>/', views.ShopView, name='shop-view'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('openapi/', get_schema_view(title="Snippets API", default_version = "v1", description="Descriiption"), name='openapi-schema'),
    # path('docs/', yasg_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', TemplateView.as_view(template_name='documentation.html', extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
    path('swagger<format>/', yasg_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', yasg_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', yasg_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]





'''




urlpatterns = [
    path('api/organizations/', views.OrganizationListView, name='organizations-list'),
    path('api/organizations/<int:id>/shops_file/', views.shops_file, name='get-shops-file'),
    path('api/shops/<int:id>/', views.ShopView, name='shop-view'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('docs/', yasg_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]











urlpatterns = [
    path('api/organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('api/organizations/<int:id>/shops_file/', download_shops_file.as_view(), name='get-shops-file'),
    path('api/shops/<int:id>/', ShopView.as_view(), name='shop-view'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('docs/', yasg_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]




'''



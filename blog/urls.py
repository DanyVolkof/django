"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import ShopView
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

yasg_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version = "v1",
        description = "Descriiption",
        terms_of_service = "https://www.google.com/policies/terms/",
        contact = opebapi.Contact(email="contact@snippets.local"),
        license = openapi.license(name="BSD Licence"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('api/shops/<int:id>/', ShopDetail.as_view(), name='shop-view'),
    path('organizations/<int:id>/shops_file/', download_shops_file, name='get-shops-file'),
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/shop/<int:id>/', put, name='put'),
]

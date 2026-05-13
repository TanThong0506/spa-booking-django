"""
URL configuration for spa_booking project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from services.views import home
from spa_booking.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health endpoints (support both with and without trailing slash)
    path('api/health', health_check, name='health_check_no_slash'),
    path('api/health/', health_check, name='health_check'),

    # API Endpoints
    path('api/', include('spa_booking.api_urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('services/', include('services.urls')),
    path('appointments/', include('appointments.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('user/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
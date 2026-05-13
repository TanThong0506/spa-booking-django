"""
API URL Configuration for Spa Booking
"""
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

# Import ViewSets
from accounts.views import ProfileViewSet
from appointments.views import AppointmentViewSet
from services.views import ServiceViewSet

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

# API URL patterns
api_urlpatterns = [
    # API Documentation
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # ViewSets
    path('', include(router.urls)),
]

urlpatterns = api_urlpatterns

from django.urls import path

from .views import service_list, service_suggestions

urlpatterns = [
    path('', service_list, name='service_list'),
    path('suggestions/', service_suggestions, name='service_suggestions'),
]
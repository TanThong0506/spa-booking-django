from django.urls import path
from .views import create_appointment, my_appointments, cancel_appointment

urlpatterns = [
    path('create/', create_appointment, name='create_appointment'),
    path('my/', my_appointments, name='my_appointments'),
    path('cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
]
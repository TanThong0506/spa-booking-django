from django.urls import path
from .views import dashboard, update_appointment_status, assign_to_me

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('update-status/<int:appointment_id>/<str:status>/', update_appointment_status, name='update_appointment_status'),
    path('assign/<int:appointment_id>/', assign_to_me, name='assign_to_me'),
]
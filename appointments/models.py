# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from services.models import Service


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    employee = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='assigned_appointments'
)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"
    
class Meta:
    verbose_name = "Lịch hẹn"
    verbose_name_plural = "Lịch hẹn"
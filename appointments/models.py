from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError # Thêm dòng này
from django.utils import timezone # Thêm dòng này
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

    # --- ĐÂY LÀ PHẦN FIX LỖI (SRE/QA Task) ---
    def clean(self):
        # Kiểm tra nếu ngày đặt lịch nhỏ hơn ngày hiện tại
        if self.appointment_date < timezone.now().date():
            raise ValidationError({'appointment_date': "Không thể đặt lịch cho ngày trong quá khứ!"})

    def save(self, *args, **kwargs):
        self.full_clean() # Bắt buộc gọi full_clean để chạy hàm clean() ở trên
        super().save(*args, **kwargs)
    # ----------------------------------------

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"

    class Meta: # Nhớ lùi đầu dòng class Meta này vào trong class Appointment
        verbose_name = "Lịch hẹn"
        verbose_name_plural = "Lịch hẹn"
from django import forms
from django.utils import timezone
from datetime import time
from .models import Appointment


TIME_CHOICES = [
    ('08:00', '08:00'),
    ('08:30', '08:30'),
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
    ('18:00', '18:00'),
]


class AppointmentForm(forms.ModelForm):
    appointment_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        label='Giờ hẹn'
    )

    class Meta:
        model = Appointment
        fields = ['customer_name', 'customer_phone', 'service', 'appointment_date', 'appointment_time', 'note']

        labels = {
            'customer_name': 'Họ tên người đặt',
            'customer_phone': 'Số điện thoại',
            'service': 'Dịch vụ',
            'appointment_date': 'Ngày hẹn',
            'note': 'Ghi chú',
        }

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Nhập ghi chú nếu có...'}),
        }

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')

        if not phone:
            raise forms.ValidationError("Vui lòng nhập số điện thoại.")

        if not phone.isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa chữ số.")

        if len(phone) < 9 or len(phone) > 11:
            raise forms.ValidationError("Số điện thoại không hợp lệ.")

        return phone

    class Meta:
        model = Appointment
        fields = ['customer_name', 'customer_phone', 'service', 'appointment_date', 'appointment_time', 'note']

        labels = {
            'service': 'Dịch vụ',
            'appointment_date': 'Ngày hẹn',
            'note': 'Ghi chú',
            'customer_name': 'Họ tên người đặt',
            'customer_phone': 'Số điện thoại',
        }

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Nhập ghi chú nếu có...'}),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        today = timezone.localdate()

        if appointment_date < today:
            raise forms.ValidationError("Không thể đặt lịch cho ngày đã qua.")

        return appointment_date

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')

        hour, minute = map(int, appointment_time.split(':'))
        appointment_time = time(hour, minute)

        start_time = time(8, 0)
        end_time = time(18, 0)

        if appointment_time < start_time or appointment_time > end_time:
            raise forms.ValidationError("Chỉ được đặt lịch từ 08:00 đến 18:00.")

        return appointment_time
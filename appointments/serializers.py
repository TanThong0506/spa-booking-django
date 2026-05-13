from django.contrib.auth.models import User
from rest_framework import serializers

from services.models import Service
from services.serializers import ServiceSerializer

from .models import Appointment


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class AppointmentSerializer(serializers.ModelSerializer):
    customer = UserMinimalSerializer(read_only=True)
    employee = UserMinimalSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='employee',
        write_only=True,
        required=False,
        allow_null=True
    )
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )
    status_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone',
            'employee', 'employee_id', 'service', 'service_id',
            'appointment_date', 'appointment_time', 'note', 'status',
            'status_display', 'duration_display', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_status_display(self, obj):
        status_colors = {
            'pending': '🟡 Pending',
            'confirmed': '✅ Confirmed',
            'completed': '✔️ Completed',
            'cancelled': '❌ Cancelled'
        }
        return status_colors.get(obj.status, obj.status)

    def get_duration_display(self, obj):
        if obj.service:
            return f'{obj.service.duration} minutes'
        return '-'

    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_phone = validated_data.get('customer_phone', instance.customer_phone)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.service = validated_data.get('service', instance.service)
        instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        instance.appointment_time = validated_data.get('appointment_time', instance.appointment_time)
        instance.note = validated_data.get('note', instance.note)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class AppointmentListSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'customer_name', 'customer_phone', 'service_name',
            'employee_name', 'appointment_date', 'appointment_time',
            'status', 'status_display'
        ]

    def get_status_display(self, obj):
        status_colors = {
            'pending': '🟡 Pending',
            'confirmed': '✅ Confirmed',
            'completed': '✔️ Completed',
            'cancelled': '❌ Cancelled'
        }
        return status_colors.get(obj.status, obj.status)


class AppointmentStatisticsSerializer(serializers.Serializer):
    total_appointments = serializers.IntegerField()
    pending = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    completed = serializers.IntegerField()
    cancelled = serializers.IntegerField()

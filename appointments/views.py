from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Appointment
from .serializers import (
    AppointmentSerializer, AppointmentListSerializer, AppointmentStatisticsSerializer
)

@login_required
def my_appointments(request):
    appointments = request.user.appointment_set.all()
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})
    
def create_appointment(request):
    service_id = request.GET.get('service_id')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.save()
            messages.success(request, "Đặt lịch thành công. Vui lòng chờ nhân viên xác nhận.")
            return redirect('my_appointments')
    else:
        initial_data = {}

        if service_id:
            initial_data['service'] = service_id

        form = AppointmentForm(initial=initial_data)

    return render(request, 'appointments/create_appointment.html', {'form': form})


# ==================== API ViewSets ====================

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing spa appointments.
    
    - GET /api/appointments/ - List all appointments (staff) or user's appointments
    - GET /api/appointments/{id}/ - Get specific appointment
    - POST /api/appointments/ - Create new appointment
    - PUT /api/appointments/{id}/ - Update appointment (owner or staff)
    - DELETE /api/appointments/{id}/ - Cancel appointment (owner or staff)
    - GET /api/appointments/my_appointments/ - Get current user's appointments
    - GET /api/appointments/statistics/ - Get appointment statistics (staff only)
    """
    permission_classes = [IsAuthenticated]
    search_fields = ['customer_name', 'customer_phone', 'service__name', 'employee__username']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at', 'status']
    ordering = ['-appointment_date', '-appointment_time']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(Q(customer=user) | Q(employee=user))

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentListSerializer
        elif self.action == 'retrieve':
            return AppointmentSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        appointment = self.get_object()
        if not (self.request.user.is_staff or self.request.user == appointment.customer):
            raise PermissionDenied('You can only update your own appointments')
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or self.request.user == instance.customer):
            raise PermissionDenied('You can only cancel your own appointments')
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_appointments(self, request):
        """Get current user's appointments"""
        appointments = Appointment.objects.filter(customer=request.user)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Get appointment statistics"""
        total = Appointment.objects.count()
        pending = Appointment.objects.filter(status='pending').count()
        confirmed = Appointment.objects.filter(status='confirmed').count()
        completed = Appointment.objects.filter(status='completed').count()
        cancelled = Appointment.objects.filter(status='cancelled').count()

        data = {
            'total_appointments': total,
            'pending': pending,
            'confirmed': confirmed,
            'completed': completed,
            'cancelled': cancelled,
        }
        serializer = AppointmentStatisticsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending(self, request):
        """Get pending appointments"""
        appointments = Appointment.objects.filter(status='pending')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def today(self, request):
        """Get today's appointments"""
        today = datetime.now().date()
        appointments = Appointment.objects.filter(appointment_date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def upcoming(self, request):
        """Get upcoming appointments (next 7 days)"""
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        appointments = Appointment.objects.filter(
            appointment_date__gte=today,
            appointment_date__lte=next_week
        ).order_by('appointment_date', 'appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def confirm(self, request, pk=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def complete(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        if not (request.user.is_staff or request.user == appointment.customer):
            return Response(
                {'detail': 'You can only cancel your own appointments'},
                status=status.HTTP_403_FORBIDDEN
            )
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = request.user.appointment_set.get(id=appointment_id)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, "Hủy lịch thành công.")
    return redirect('my_appointments')
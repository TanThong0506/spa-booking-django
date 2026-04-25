from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment


def dashboard(request):
    if not is_employee_or_admin(request.user):
        return redirect('service_list')

    total = Appointment.objects.count()
    pending = Appointment.objects.filter(status='pending').count()
    confirmed = Appointment.objects.filter(status='confirmed').count()
    completed = Appointment.objects.filter(status='completed').count()
    cancelled = Appointment.objects.filter(status='cancelled').count()

    appointments = Appointment.objects.all().order_by('-created_at')

    context = {
        'total': total,
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'cancelled': cancelled,
        'appointments': appointments,
    }

    return render(request, 'dashboard/dashboard.html', context)

def is_employee_or_admin(user):
    if user.is_staff:
        return True

    if hasattr(user, 'profile') and user.profile.role == 'employee':
        return True

    return False

def update_appointment_status(request, appointment_id, status):
    if not is_employee_or_admin(request.user):
        return redirect('service_list')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.status in ['cancelled', 'completed']:
        return redirect('dashboard')
    
    if status in ['confirmed', 'completed'] and appointment.employee is None:
        appointment.employee = request.user
    appointment.status = status
    appointment.save()

    return redirect('dashboard')

def assign_to_me(request, appointment_id):
    if not is_employee_or_admin(request.user):
        return redirect('service_list')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.status not in ['cancelled', 'completed']:
        appointment.employee = request.user
        appointment.save()

    return redirect('dashboard')
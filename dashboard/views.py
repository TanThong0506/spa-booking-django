from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment


def dashboard(request):
    if not request.user.is_staff:
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


def update_appointment_status(request, appointment_id, status):
    if not request.user.is_staff:
        return redirect('service_list')

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.status in ['cancelled', 'completed']:
        return redirect('dashboard')

    appointment.status = status
    appointment.save()

    return redirect('dashboard')
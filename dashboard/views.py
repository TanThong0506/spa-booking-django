from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

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

    today = timezone.localdate()

    total_revenue = Appointment.objects.filter(
        status='completed'
    ).aggregate(total=Sum('service__price'))['total'] or 0

    today_revenue = Appointment.objects.filter(
        status='completed',
        appointment_date=today
    ).aggregate(total=Sum('service__price'))['total'] or 0

    today_appointments = Appointment.objects.filter(
        appointment_date=today
    ).count()

    context = {
        'total': total,
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'cancelled': cancelled,
        'appointments': appointments,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'today_appointments': today_appointments,
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

def revenue_view(request):
    if not request.user.is_staff:
        return redirect('service_list')

    today = timezone.localdate()

    selected_date = request.GET.get('date')
    selected_month = request.GET.get('month')

    if selected_date:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = today

    if selected_month:
        year, month = map(int, selected_month.split('-'))
    else:
        year = today.year
        month = today.month

    day_revenue = Appointment.objects.filter(
        status='completed',
        appointment_date=selected_date
    ).aggregate(total=Sum('service__price'))['total'] or 0

    month_revenue = Appointment.objects.filter(
        status='completed',
        appointment_date__year=year,
        appointment_date__month=month
    ).aggregate(total=Sum('service__price'))['total'] or 0

    day_appointments = Appointment.objects.filter(
        status='completed',
        appointment_date=selected_date
    )

    month_appointments = Appointment.objects.filter(
        status='completed',
        appointment_date__year=year,
        appointment_date__month=month
    )

    return render(request, 'dashboard/revenue.html', {
        'selected_date': selected_date,
        'selected_month': f"{year}-{month:02d}",
        'day_revenue': day_revenue,
        'month_revenue': month_revenue,
        'day_appointments': day_appointments,
        'month_appointments': month_appointments,
    })
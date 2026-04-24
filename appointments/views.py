from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm

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
            return redirect('my_appointments')
    else:
        initial_data = {}

        if service_id:
            initial_data['service'] = service_id

        form = AppointmentForm(initial=initial_data)

    return render(request, 'appointments/create_appointment.html', {'form': form})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = request.user.appointment_set.get(id=appointment_id)
    appointment.status = 'cancelled'
    appointment.save()
    return redirect('my_appointments')
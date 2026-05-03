from django.shortcuts import render
from .models import Service
from django.http import JsonResponse

def service_list(request):
    keyword = request.GET.get('q')

    services = Service.objects.filter(is_active=True)

    if keyword:
        services = services.filter(name__icontains=keyword)

    return render(request, 'services/service_list.html', {
        'services': services,
        'keyword': keyword,
    })

def service_suggestions(request):
    keyword = request.GET.get('q', '')

    services = Service.objects.filter(
        is_active=True,
        name__icontains=keyword
    ).values_list('name', flat=True)[:8]

    return JsonResponse(list(services), safe=False)

def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'services/home.html', {
        'services': services
    })
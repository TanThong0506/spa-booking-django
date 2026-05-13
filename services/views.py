from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Service
from .serializers import (
    ServiceDetailSerializer,
    ServiceListSerializer,
    ServiceSerializer,
)


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


# ==================== API ViewSets ====================

class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing spa services.
    
    - GET /api/services/ - List all active services (paginated)
    - GET /api/services/{id}/ - Get specific service
    - POST /api/services/ - Create new service (admin only)
    - PUT /api/services/{id}/ - Update service (admin only)
    - DELETE /api/services/{id}/ - Delete service (admin only)
    - GET /api/services/active/ - Get active services only
    - GET /api/services/inactive/ - Get inactive services (admin only)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'duration', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'inactive']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Service.objects.all()
        return Service.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        elif self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied('Only staff can create services')
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied('Only staff can update services')
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied('Only staff can delete services')
        instance.delete()

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active services"""
        services = Service.objects.filter(is_active=True)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def inactive(self, request):
        """Get all inactive services"""
        services = Service.objects.filter(is_active=False)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)
from django.shortcuts import render, redirect
from .forms import RegisterForm
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile
from .serializers import ProfileSerializer, ProfileDetailSerializer


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# ==================== API ViewSets ====================

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user profiles.
    
    - GET /api/profiles/ - List all profiles (paginated)
    - GET /api/profiles/{id}/ - Get specific profile
    - POST /api/profiles/ - Create new profile (admin only)
    - PUT /api/profiles/{id}/ - Update profile
    - DELETE /api/profiles/{id}/ - Delete profile (admin only)
    - GET /api/profiles/me/ - Get current user's profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__username', 'user__email', 'phone', 'role']
    ordering_fields = ['user__username', 'role', 'id']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileDetailSerializer
        return ProfileSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found for current user'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def employees(self, request):
        """Get all employees"""
        profiles = Profile.objects.filter(role='employee')
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def customers(self, request):
        """Get all customers"""
        profiles = Profile.objects.filter(role='customer')
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)
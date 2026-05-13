from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'formatted_price', 'duration', 'image', 'is_active', 'status_display', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_status_display(self, obj):
        return '✅ Active' if obj.is_active else '❌ Inactive'

    def get_formatted_price(self, obj):
        return f'{obj.price:,.0f} VND' if obj.price else '-'


class ServiceDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'formatted_price', 'duration', 'image', 'is_active', 'status_display', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_status_display(self, obj):
        return '✅ Active' if obj.is_active else '❌ Inactive'

    def get_formatted_price(self, obj):
        return f'{obj.price:,.0f} VND' if obj.price else '-'


class ServiceListSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'formatted_price', 'duration', 'is_active']
        read_only_fields = ['id']

    def get_formatted_price(self, obj):
        return f'{obj.price:,.0f} VND' if obj.price else '-'

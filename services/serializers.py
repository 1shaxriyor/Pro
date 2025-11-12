# services/serializers.py
from rest_framework import serializers
from .models import Service, Master

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Master
        fields = ['id', 'name', 'phone', 'service', 'service_name']

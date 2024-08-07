from rest_framework import serializers
from .models import ArtiLes

class ArtiLesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtiLes
        fields = '__all__'
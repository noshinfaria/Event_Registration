# events/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventRegistration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 
            'title', 
            'description', 
            'date', 
            'time', 
            'location_name',
            'available_slots',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventRegistration
        fields = ['id', 'event']

    def get_event(self, obj):
        return EventSerializer(obj.event).data
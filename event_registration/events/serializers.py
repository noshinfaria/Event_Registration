# events/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventRegistration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class EventRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'timestamp']
from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'location_name']
    search_fields = ['title', 'location_name']
    list_filter = ['date', 'time']


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'timestamp']
    search_fields = ['event']
    list_filter = ['event', 'timestamp']

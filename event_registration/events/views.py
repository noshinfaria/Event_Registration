# events/views.py
from django.shortcuts import render
from rest_framework import generics
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.urls import reverse
from rest_framework.filters import SearchFilter




# class EventListCreateView(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     template_name = 'events/event_list.html'


# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['title', 'description', 'location_name']

#     def get_queryset(self):
#         print("Search term:", self.request.query_params.get('search'))
#         queryset = super().get_queryset()
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = Event.objects.all()
#         return render(request, 'events/event_list.html', {'queryset': queryset})

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         return render(request, 'events/event_detail.html', {'event': instance})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'location_name']

    def get_queryset(self):
        print("Search term:", self.request.query_params.get('search'))
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Use the filtered queryset
        return render(request, 'events/event_list.html', {'queryset': queryset})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return render(request, 'events/event_detail.html', {'event': instance})
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_slots > 0:
        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            messages.warning(request, 'You have already registered for this event.')
        else:
            EventRegistration.objects.create(user=request.user, event=event)
            event.available_slots -= 1
            event.save()
            messages.success(request, 'Event booked successfully.')
    else:
        messages.error(request, 'No available slots for this event.')

    return redirect('event-detail', pk=event_id)


class UserRegisteredEventsAPIView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return EventRegistration.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        context = {'registered_events': serializer.data}
        return render(request, 'events/user_registered_events.html', context)

    

class UnregisterFromEventAPIView(generics.DestroyAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return EventRegistration.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        event = instance.event
        event.available_slots += 1
        event.save()
        instance.delete()
        return redirect('registered-events')
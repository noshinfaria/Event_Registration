# events/views.py
from rest_framework import generics
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status



class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegistrationView(generics.CreateAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    def create(self, request, *args, **kwargs):
        event_id = self.kwargs.get('pk')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        if event.available_slots > 0:
            user = self.request.user
            registration, created = EventRegistration.objects.get_or_create(user=user, event=event)

            if created:
                event.available_slots -= 1
                event.save()
                return Response(EventRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User already registered for this event"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No available slots for this event"}, status=status.HTTP_400_BAD_REQUEST)

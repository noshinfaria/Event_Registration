from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location_name = models.CharField(max_length=255)
    total_slots = models.PositiveIntegerField(default=0)
    available_slots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.total_slots < 0:
            self.total_slots = 0
        if self.available_slots > self.total_slots:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"

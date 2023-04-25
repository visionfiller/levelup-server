from django.db import models


class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='events')
    location = models.CharField(max_length=155)
    description = models.CharField(max_length=155)
    attendees = models.ManyToManyField("Gamer")
    date = models.DateField()
    time = models.TimeField()
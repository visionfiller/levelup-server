from django.db import models



class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='events')
    location = models.CharField(max_length=155)
    description = models.CharField(max_length=155)
    attendees = models.ManyToManyField("Gamer", related_name='attendees')
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
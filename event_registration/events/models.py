from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='event_photos/')

    def __str__(self):
        return self.name
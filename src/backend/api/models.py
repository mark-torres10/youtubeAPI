from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    channel = models.ForeignKey(Channel, related_name='episodes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from django.db import models

# Create your models here.


class Listing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=512)


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=512)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=512)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

from audioop import maxpp
from tkinter import CASCADE
from django.db import models

# Create your models here.

class RouteName(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self) :
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=256)
    vehicleNumber = models.IntegerField(max_length=256)
    route= models.CharField(max_length=256)
    distance = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name


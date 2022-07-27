from email.headerregistry import Address
from django.db import models
from statistics import mode
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Flush(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opration_hours = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    #unique characteristics
    gender_neutral = models.CharField(max_length=15)
    special_needs = models.CharField(max_length=15)
    baby_station = models.CharField(max_length=15)
    family_restroom = models.CharField(max_length=15)
    
    price = models.IntegerField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return self.name
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'flush_id': self.id})

    # def score_for_today(self):
    #     return self.feedback_set.filter(date=date.today()).count() >= len(SCORES)
from django.db import models
from statistics import mode
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

##################################
# Flush Model
##################################

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
        return f"{self.name} - {self.address}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'flush_id': self.id})

    # def score_for_today(self):
    #     return self.feedback_set.filter(date=date.today()).count() >= len(SCORES)

##################################
# Comment Model
##################################

class Comment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    flush = models.ForeignKey(Flush, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

##################################
# Photo Model
##################################

class Photo(models.Model):
    url = models.CharField(max_length=300)
    flush = models.ForeignKey(Flush, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for flush_id: {self.flush_id} @{self.url}'
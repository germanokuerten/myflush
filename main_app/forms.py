from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from .models import Comment

class CommentForm(ModelForm):
    class Meta: 
        model = Comment
        fields = ['title', 'content']
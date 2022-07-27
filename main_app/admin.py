from django.contrib import admin
from .models import Flush, Comment, Photo

# Register your models here.

admin.site.register(Flush)
admin.site.register(Comment)
admin.site.register(Photo)
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('flushes/', views.flushes_index, name='flushes'),
    path('flushes/<int:flush_id>/', views.flushes_detail, name='detail'),
    path('flushes/create/', views.FlushCreate.as_view(), name='flushes_create'),
]


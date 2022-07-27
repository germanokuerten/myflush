from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('flushes/', views.flushes_index, name='flushes'),
    path('flushes/<int:flush_id>/', views.flushes_detail, name='detail'),
    path('flushes/create/', views.FlushCreate.as_view(), name='flushes_create'),
    path('flushes/<int:pk>/update/', views.FlushUpdate.as_view(), name='flushes_update'),
    path('flushes/<int:pk>/delete/', views.FlushDelete.as_view(), name='flushes_delete'),
    
    path('flushes/<int:flush_id>/add_comment/', views.add_comment, name='add_comment'),
    path('flushes/<int:flush_id>/add_photo/', views.add_photo, name='add_photo'),
    
]


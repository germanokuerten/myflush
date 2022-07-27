from django.shortcuts import render
from django.http import HttpResponse
from .models import Flush

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def flushes_index(request):
    flushes = Flush.objects.order_by('id')
    return render(request, 'flushes/index.html', {'flushes': flushes})

def flushes_detail(request, flush_id):
		# Get the individual "flush"
    flush = Flush.objects.get(id=flush_id)
    return render(request, 'flushes/detail.html', {'flush': flush})
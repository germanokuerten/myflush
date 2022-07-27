from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

class FlushCreate(CreateView):
    model = Flush
    fields = '__all__'
    success_url = '/flushes/'

class FlushUpdate(UpdateView):
    model = Flush
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = '__all__'

class FlushDelete(DeleteView):
    model = Flush
    success_url = '/flushes/'


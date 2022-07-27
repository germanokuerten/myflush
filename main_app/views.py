from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Flush
from .forms import CommentForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

##################################
# Flush Functions and Classes
##################################

def flushes_index(request):
    flushes = Flush.objects.order_by('id')
    return render(request, 'flushes/index.html', {'flushes': flushes})

def flushes_detail(request, flush_id):
		# Get the individual "flush"
    flush = Flush.objects.get(id=flush_id)
    comment_form = CommentForm()
    return render(request, 'flushes/detail.html', {'flush': flush, 'comment_form': comment_form})

class FlushCreate(CreateView):
    model = Flush
    fields = ['name', 'contact', 'address', 'opration_hours', 'description', 'gender_neutral', 'special_needs', 'baby_station', 'family_restroom', 'price']
    success_url = '/flushes/'

class FlushUpdate(UpdateView):
    model = Flush
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = '__all__'

class FlushDelete(DeleteView):
    model = Flush
    success_url = '/flushes/'

##################################
# Reviews Functions and Classes
##################################

def add_comment(request, flush_id):
	# create the ModelForm using the data in request.POST
  form = CommentForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_comment = form.save(commit=False)
    new_comment.flush_id = flush_id
    new_comment.save()
  return redirect('detail', flush_id=flush_id)
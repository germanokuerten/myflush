from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Flush, Comment, Photo
from .forms import CommentForm
import uuid 
import boto3

# Amazon AWS S3 - Settings
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'myflush'

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

##################################
# Reviews Functions and Classes
##################################  

def add_photo(request, flush_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, flush_id=flush_id)
            photo.save()
        except:
            print('An error occurred - S3')
    return redirect('detail', flush_id=flush_id)
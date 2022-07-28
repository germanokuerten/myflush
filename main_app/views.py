from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from .models import Flush, Photo
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

@login_required
def flushes_index(request):
    flushes = Flush.objects.order_by('id')
    return render(request, 'flushes/index.html', {'flushes': flushes})

@login_required
def flushes_detail(request, flush_id):
		# Get the individual "flush"
    flush = Flush.objects.get(id=flush_id)
    comment_form = CommentForm()
    return render(request, 'flushes/detail.html', {'flush': flush, 'comment_form': comment_form})

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/flushes')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)

class FlushCreate(LoginRequiredMixin, CreateView):
    model = Flush
    fields = ['name', 'contact', 'address', 'opration_hours', 'description', 'gender_neutral', 'special_needs', 'baby_station', 'family_restroom', 'price']
    success_url = '/flushes/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FlushUpdate(UserAccessMixin, UpdateView):

    raise_exception = False
    permission_required = 'flush.change_flushes'
    login_url = '/flushes/'

    model = Flush
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = '__all__'

class FlushDelete(UserAccessMixin, DeleteView):
    permission_required = 'flush.change_flushes'
    model = Flush
    success_url = '/flushes/'

##################################
# Review Function
##################################

@login_required
def add_comment(request, flush_id, user_id):
	# create the ModelForm using the data in request.POST
  form = CommentForm(request.POST)
  print(form)
  
  new_comment = form.save(commit=False)
  new_comment.flush_id = flush_id
  new_comment.user_id = user_id
  new_comment.save()
  return redirect('detail', flush_id=flush_id)

##################################
# Add Photo Function
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

##################################
# SignUp Function
################################## 

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('flushes')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def flushes_index(request):
    return render(request, 'flushes/index.html', {'flushes': flushes})

# Faux Flush Data - Database simulation
class Flush:
    def __init__(self, name, contact, operation_hours, price):
        self.name = name
        self.contact = contact
        self.operation_hours = operation_hours
        self.price = price

# Book objects that are being instantiated from the Book class.
flushes = [
    Flush('Rich Dad Poor Dad', 'Robert T. Kiyosaki', ' What the Rich Teach Their Kids About Money That the Poor and Middle Class Do Not!', 7),
    Flush('Think and Grow Rich', 'Napoleon Hill', '"Think and Grow Rich" is a motivational personal development and self-help book written by Napoleon Hill and inspired by a suggestion from Scottish-American businessman Andrew Carnegie."', 15),
    Flush('The Alchemist', 'Paulo Coelho', 'A Fable About Following Your Dream', 14),
]
from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1>REST REST and REST</h1>')
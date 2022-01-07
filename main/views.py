from django.shortcuts import render
from .serializers import articleSerializer
from .models import article
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from main.models import article

# Create your views here.

def home(request):
    return render(request,'main/home.html')

def serializeddata(request):
    articles = article.objects.all()
    serialized = articleSerializer(articles,many=True)

    json_data= JSONRenderer().render(serialized.data)

    return HttpResponse(json_data,content_type='application/json')
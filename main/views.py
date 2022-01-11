from django.shortcuts import render
from .serializers import articleSerializer
from .models import article
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request,'main/home.html')

def serializeddata(request):
    articles = article.objects.all()
    serialized = articleSerializer(articles,many=True)

    json_data= JSONRenderer().render(serialized.data)

    return HttpResponse(json_data,content_type='application/json')

def get(request,id):
    if article.objects.filter(idd=id).exists():
        articles = article.objects.get(idd=id)
        print(articles)
        serialized = articleSerializer(articles)
        json_data = JSONRenderer().render(serialized.data)
        return HttpResponse(json_data,content_type='application/json')
    else:
        return HttpResponse('Bad Request',content_type='application/json')
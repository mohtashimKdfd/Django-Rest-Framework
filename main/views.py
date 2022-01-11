from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from .serializers import articleSerializer
from .models import article
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    return render(request,'main/home.html')

@csrf_exempt
def serializeddata(request):
    if request.method == 'GET':
        articles = article.objects.all()
        serialized = articleSerializer(articles,many=True)

        json_data= JSONRenderer().render(serialized.data)

        return HttpResponse(json_data,content_type='application/json')
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = articleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

def get(request,id):
    if request.method == 'GET':
        if article.objects.filter(idd=id).exists():
            articles = article.objects.get(idd=id)
            print(articles)
            serialized = articleSerializer(articles)
            json_data = JSONRenderer().render(serialized.data)
            return HttpResponse(json_data,content_type='application/json')
        else:
            return HttpResponse('Bad Request',content_type='application/json')
from django.http.response import JsonResponse
from django.shortcuts import render
from .serializers import articleSerializer
from .models import article
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def home(request):
    return render(request,'main/home.html')

# @csrf_exempt
# def serializeddata(request):
#     if request.method == 'GET':
#         articles = article.objects.all()
#         serialized = articleSerializer(articles,many=True)

#         # json_data= JSONRenderer().render(serialized.data)

#         return JsonResponse(serialized.data,safe=False)
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = articleSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors,status=400)

#Same thing but making the use of api_view decorator
@api_view(['GET','POST'])
def serializeddata(request):
    if request.method == 'GET':
        articles = article.objects.all()
        serialized = articleSerializer(articles,many=True)
        return Response(serialized.data)

    elif request.method == "POST":
        # data = JSONParser().parse(request)
        serializer = articleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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

@csrf_exempt
def articleDetails(request,pk):
    try:
        targetArticle = article.objects.get(idd=pk)

    except article.DoesNotExist:
        return HttpResponse("Data not found",content_type='application/json')
    
    if request.method == 'GET':
        serializer = articleSerializer(targetArticle)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = articleSerializer(targetArticle,data=data)
        
        #check if the serialized data is valid

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data,status=201)
        return HttpResponse(serializer.errors,status=400)
    
    elif request.method == 'DELETE':
        targetArticle.delete()
        return HttpResponse(status=204)
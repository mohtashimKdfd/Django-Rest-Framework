from django.http.response import JsonResponse
from django.shortcuts import render
from .serializers import articleSerializer
from .models import article
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics

#For Authentications
from rest_framework.authentication import BasicAuthentication , SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly , DjangoModelPermissions


#ListModelMixin = used to give all data from database
#CreateModelMixin = used to update data in database
class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = articleSerializer
    queryset = article.objects.all()

    lookup_field = 'id'

    authentication_classes = [SessionAuthentication,BasicAuthentication]
    # authentication_classes = [TokenAuthentication]

    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [DjangoModelPermissions]


    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self,request):
        return self.create(request)
    
    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)


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
# @authentication_classes([TokenAuthentication])
# @authentication_classes([BasicAuthentication,SessionAuthentication])
# @permission_classes([IsAuthenticatedOrReadOnly])
# @permission_classes([IsAuthenticated])
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

# permisssion_classes = [AllowAny] is used to allow any user ro read/write and is also used to override global authentication

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


# #using api_view thing

# @api_view(['GET','PUT','DELETE'])
# def articleDetails(request,pk):
#     try:
#         targetArticle = article.objects.get(idd=pk)

#     except article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = articleSerializer(targetArticle)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         serializer = articleSerializer(targetArticle,data=request.data)
        
#         #check if the serialized data is valid

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         targetArticle.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

##########***************************************************************###########
#Using class based Views

class ArticleAPIView(APIView):
    # def home(self,request):
    #     return render(request,'main/home.html')

    def get(self,request):
        articles = article.objects.all()
        serialized = articleSerializer(articles,many=True)

        return JsonResponse(serialized.data,safe=False)
    
    def post(self,request):
        data = JSONParser().parse(request)
        serialiazed = articleSerializer(data=data)

        if serialiazed.is_valid():
            serialiazed.save()
            return JsonResponse(serialiazed.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serialiazed.errors,status=status.HTTP_400_BAD_REQUEST)

class ArticleDetalsAPIView(APIView):
    def get_object(self,pk):
        try:
            return article.objects.get(idd=pk)

        except article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        try:
            targetArticle = self.get_object(pk)
            serialized = articleSerializer(targetArticle)

            return JsonResponse(serialized.data)
        except:
            return HttpResponse('Not Found',status=status.HTTP_404_NOT_FOUND,content_type='application/json')
    
    def put(self,request,pk):
        # data = JSONParser().parse(request)
        targetArticle = self.get_object(pk)
        serialized = articleSerializer(targetArticle,data=request.data)

        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data,status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        targetArticle = self.get_object(pk)
        targetArticle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        


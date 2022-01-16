from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get',views.serializeddata),
    path('gett/<int:id>',views.get),
    # path('details/<int:pk>',views.articleDetails),
    path('details/<int:pk>',views.ArticleDetalsAPIView.as_view()),
    path('get',views.ArticleAPIView.as_view()),
    path('generic/get/<int:id>',views.GenericAPIView.as_view()),
    path('auth',include('rest_framework.urls'),name='rest_framework')
]

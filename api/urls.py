from django.urls import path
from .views import *
app_name = "api"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', ArticleListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', ArticleRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
     path('posts/<int:pk>/like/', LikeArticleView.as_view(), name='like-article'),
]
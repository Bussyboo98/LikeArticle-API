from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .permissions import *
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        data = {
            'user_id': user.id,'username': user.username,
            'email': user.email,'refresh': str(refresh),
            'access': str(access_token),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful", 'user_id': user.id,
                "token": token.key,"username" : username})
        else:
            return Response({"error": "Invalid credentials."}, status=401)
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Delete the user's token
            return Response({"message": "Successfully logged out."}, status=200)
        except (AttributeError, Token.DoesNotExist):
            return Response({"message": "Logout failed."}, status=400)


class LikeArticleView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
       
        like = serializer.save(user=request.user)
        article = like.article  
        
        
        data = {
            "message": f"You have liked the article: '{article.title}'",
            "article": article.id,
            "like_count": article.like_article_count
        }
        return Response(data, status=status.HTTP_201_CREATED)
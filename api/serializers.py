from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password",
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator()]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = { 'username': {'required': True}, }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user) 
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        write_only=True,
        max_length=150
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(
        read_only=True
    )
    user_id = serializers.IntegerField(
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")

        attrs['user'] = user
        attrs['token'] = Token.objects.get(user=user).key  
        attrs['user_id'] = user.id
        return attrs
    


class ArticleSerializer(serializers.ModelSerializer):
    like_article_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'like_article_count']
        

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
         model = LikeArticle
         fields =['article']
         
    def create(self, validated_data):
        user = self.context['request'].user     
        article =  validated_data['article']
        
        like, created = LikeArticle.objects.get_or_create(user=user, article=article)
        
        if not created:
            raise serializers.ValidationError("You have liked this post already")
        
        
        article.like_article_count += 1
        article.save()
        
        return like
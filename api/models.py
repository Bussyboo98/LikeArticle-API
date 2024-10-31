from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField



class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = HTMLField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    like_article_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title
    
class LikeArticle(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        unique_together = ('user', 'article') 
    


from django.db import models  
from django.contrib.auth.models import User  


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField(blank=True, default='') 
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)  

    def __str__(self):  
        return f'{self.user.username} Profile'  


class Post(models.Model):  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  
    image = models.ImageField(upload_to='posts/') 
    content = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self): 
        return f'{self.author.username} - {self.content[:20]}'  


class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:  
        unique_together = ('user', 'post') 


class Comment(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self): 
        return f'{self.author.username}: {self.content[:20]}'  


class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')  
    created_at = models.DateTimeField(auto_now_add=True) 


class StoryImage(models.Model):  
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='images')  
    image = models.ImageField(upload_to='stories/')
    order = models.PositiveIntegerField(default=0) 

    class Meta:  
        ordering = ['order'] 


class Follow(models.Model): 
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') 
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')  
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        unique_together = ('follower', 'following')  
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=50,default="")
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to="Images/User",null=True,blank=True)
    eduction = models.TextField(null=True,blank=True)
    bio =  models.TextField(null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.user.username
    


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


    

class Post(models.Model):
    title = models.CharField(max_length=50) 
    body = models.TextField()
    image = models.ImageField(upload_to="Images/Post")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    username = models.CharField( max_length=50,default="")
    email = models.EmailField(max_length=254,default="")
    website = models.CharField(max_length=50,default="",null=True,blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title , self.username)
    



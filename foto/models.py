from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.




class profile(models.Model):
    
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    avater=models.ImageField(null=True,default="dr_strange.jpg")
    #embedding=models.FileField(null=True,default=None)
    uploads=models.ManyToManyField("dataset",blank=True)
    
    def __str__(self):
        return self.user.username
    

class user_images(models.Model):
    user=models.ManyToManyField(profile,blank=True)
    image=models.FileField(upload_to='target_img',null=False)

    
    

    




class dataset(models.Model):

    
    date=models.DateTimeField(null=True)
    event=models.CharField(null=True,max_length=50)
    name=models.CharField(null=True,max_length=50)
    likes=models.IntegerField(null=True,default=0)
    images = models.FileField(upload_to='images/',null=False,default="userimages\images\Screenshot_4.png")



class clubdb(models.Model):
    club_name=models.CharField(null=True,max_length=100)
    description=models.TextField(null=True)
    members=models.ManyToManyField(User,blank=True)
    image=models.FileField(upload_to='club/')
    

    

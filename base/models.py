from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	name=models.CharField(max_length=200,null=True)#Define the length max to the text | null=True -> Define this new field as a NULL in DB
	username=models.CharField(unique=True,max_length=200,null=True)#Define the length max to the text | null=True -> Define this new field as a NULL in DB
	email=models.EmailField(unique=True,null=True)#This field must be unique to each user | null=True -> Define this new field as a NULL in DB
	bio=models.TextField(null=True)#null=True -> Define this new field as a NULL in DB
	avatar=models.ImageField(null=True, default="avatar.svg")#This command is related to the "pillow" library. This library is a processing image library.

	USERNAME_FIELD='username'#Set a field that will be used in Admin Page to login 
	REQUIRED_FIELDS=[]
	#The DJANGO offers your own User model(from django.contrib.auth.models import User)
	#But, normally, people want to create their own User model according their own application.
	#So, to do that, you can use the (from django.contrib.auth.models import AbstractUser)
	#Passing "AbstractUser" as a parameter, you can create your own User model according you application. 

class Topic(models.Model):
	name=models.CharField(max_length=200)#Short string row

	def __str__(self):
		return self.name

# Create your models here.
class Room(models.Model):
	host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)#null=True -> Define this new field as a NULL in DB
	topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)#null=True -> Define this new field as a NULL in DB
	name=models.CharField(max_length=200)#Short string row
	description=models.TextField(null=True,blank=True)#Long string row
	participants=models.ManyToManyField(User,related_name='participants',blank=True)#blank=True => define that it has participants doesnt is required 
	updated=models.DateTimeField(auto_now=True)#Last updating DataTime in the room
	created=models.DateTimeField(auto_now_add=True)#Creating DataTime in the room

	class Meta:
		ordering=['-updated','-created']#['-updated','-created'] => The newest to the oldest inserts in DB will be shown in the website | ['updated','created'] => The oldest to the newest inserts in DB will be shown in the website

	def __str__(self):
		return str(self.name)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)#Last updating DataTime in the message
    created = models.DateTimeField(auto_now_add=True)#Creating DataTime in the room

    class Meta:
        ordering = ['-updated', '-created']#['-updated','-created'] => The newest to the oldest inserts in DB will be shown in the website | ['updated','created'] => The oldest to the newest inserts in DB will be shown in the website

    def __str__(self):
        return self.body[0:50]
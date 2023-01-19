from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room,User

class MyUserCreationForm(UserCreationForm):
	class Meta:
		model=User
		fields=['name','username','email','password1','password2']

class RoomForm(ModelForm):
	class Meta:
		model=Room#The model we want to create the form
		fields='__all__'#Create the input fields of Form according the attribute of Room class(host, topic... etc)
		exclude=['host','participants']#Exclude host and participants input field

class UserForm(ModelForm):
	class Meta:
		model=User
		fields=['avatar','name','username','email','bio']#The input fields that I want 
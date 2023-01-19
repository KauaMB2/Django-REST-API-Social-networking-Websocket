from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer
from base.models import Room,User,Topic
from django.contrib.auth import authenticate

@api_view(['GET'])#It defines the method the user is allowed to do in this route of API
def getRoutes(request):
	routes=[
	'GET /api',
	'GET /api/rooms',
	'GET /api/rooms/:id',
	'putRoom/:id/:username/:password/',
	'deleteRoom/:id/:username/:password/',
	'postRoom/:username/:password/',
	]
	return Response(routes)#It returns the routes of the API

@api_view(['GET'])#It defines the method the user is allowed to do in this route of API
def getRooms(request):
	rooms=Room.objects.all()#It returns all the rooms of DB
	serializer=RoomSerializer(rooms,many=True)#many=True => Saying that we want to serialize multiple objects | many=False => Saying that we want to serialize only one object 
	return Response(serializer.data)#return the data serialized

@api_view(['GET'])#It defines the method the user is allowed to do in this route of API
def getRoom(request,pk):
	room=Room.objects.get(id=pk)#It returns the selected room
	serializer=RoomSerializer(room,many=False)#many=True => Saying that we want to serialize multiple objects | many=False => Saying that we want to serialize only one object 
	return Response(serializer.data)#return the data serialized

@api_view(['DELETE'])#It defines the method the user is allowed to do in this route of API
def deleteRoom(request,pk,username,password):
	username=username.lower()#Make the letters lowercase
	try:#Try see if the user exits in DB
		user=User.objects.get(username=username)
	except:#If it doesnt exists..
		return Response(status=status.HTTP_400_BAD_REQUEST)
	user=authenticate(request, username=username,password=password)#It makes the authentication of the user
	if user is not None:
		room=Room.objects.get(id=pk)
		if room.host==user:
			room.delete()
			return Response(status=status.HTTP_100_CONTINUE)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])#It defines the method the user is allowed to do in this route of API
def putRoom(request,pk,username,password):
	username=username.lower()#Make the letters lowercase
	try:#Try see if the user exits in DB
		user=User.objects.get(username=username)
	except:#If it doesnt exists..
		return Response(status=status.HTTP_400_BAD_REQUEST)
	user=authenticate(request, username=username,password=password)#It makes the authentication of the user
	if user is not None:
		room=Room.objects.get(id=pk)#It returns the row id is iquals to primarykey(pk)
		if room.host==user:
			topic, created=Topic.objects.get_or_create(name=request.data["topic"])#If the inserted topic already was created, "created" will be False and "topic" var will receive the topic object. If the inserted topic wasnt created, "created" will be true, the object will be created in DB and "topic" receive the topic object
			room.name=request.data["name"]
			room.topic=topic
			room.description=request.data["description"]
			room.save()
			return Response(status=status.HTTP_100_CONTINUE)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])#It defines the method the user is allowed to do in this route of API
def postRoom(request,username,password):
	username=username.lower()#Make the letters lowercase
	try:#Try see if the user exits in DB
		user=User.objects.get(username=username)
	except:#If it doesnt exists..
		return Response(status=status.HTTP_400_BAD_REQUEST)
	user=authenticate(request, username=username,password=password)#It makes the authentication of the user
	if user is not None:
		topic, created=Topic.objects.get_or_create(name=request.data["topic"])#If the inserted topic already was created, "created" will be False and "topic" var will receive the topic object. If the inserted topic wasnt created, "created" will be true, the object will be created in DB and "topic" receive the topic object
		room=Room.objects.create(host=user,topic=topic,name=request.data["name"],description=request.data["description"])
		room.host=user#Set the current user as a room host
		return Response(status=status.HTTP_100_CONTINUE)
	return Response(status=status.HTTP_400_BAD_REQUEST)
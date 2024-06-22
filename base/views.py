from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm,UserForm,MyUserCreationForm

#What is the request parameter?
#The request parameter is a parameter that will say about which kind of request and user did that request

# Create your views here
def loginPage(request):
    page = 'login'
    context = {'page': page, 'error': None}
    if request.user.is_authenticated:#If user is already authenticated...
        return redirect('home')
    if request.method == "POST":
        useremail = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = None
        try:
            user = User.objects.get(username=useremail)
        except User.DoesNotExist:
            context['error'] = 'Username or password does not exist'
            return render(request, 'base/login_register.html', context)
        if user:
            user = authenticate(request, username=useremail, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context['error'] = 'Username or password does not exist'
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)#It logout the current user
    return redirect('home')

def registerPage(request):
    page='register'#page name
    form=MyUserCreationForm()#form is equal to a complete user creation form

    if request.method=="POST":#If the method be POST...
        form=MyUserCreationForm(request.POST)#form will be iquals to de data that are inserted in the inputs
        if form.is_valid():#If the inputs were correctly inserted...
            user=form.save(commit=False)#Create a user in DB and attach that new user row object in the user variable
            user.username=user.username.lower()#Make the letters lowercase
            user.save()#Save de info
            login(request,user)#It makes the login of the user
            return redirect('home')
    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q=''#It is the "?q=" value of the URL
    if request.GET.get('q')!=None:
        q=request.GET.get('q')
    #The command bellow make a SEARCH in DB em returns every rows that has the topic name, room name or room description text iquals to "q" value of URL 
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics=Topic.objects.all()[0:5]#It returns the first five topics in DB
    roomCount=rooms.count()#It returns the number of rows in base_room table
    roomMessages=Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    context={'rooms':rooms,'topics':topics,'roomMessages':roomMessages,'roomCount':roomCount}
    return render(request,'base/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        body = request.POST.get('body')
        if body.strip():  # Ensure the message body is not empty
            Message.objects.create(user=request.user,room=room,body=body)#Save information in the database
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        else:
            # Optionally handle the case where the message body is empty
            print("Empty message body")

    context = {'room': room, 'roomMessages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):#Insert in DB
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=="POST":#If the method of the request be POST...
        topic_name=request.POST.get('topic')#Get the name inserted in the topic input
        topic, created=Topic.objects.get_or_create(name=topic_name)#If the inserted topic already was created, "created" will be False and "topic" var will receive the topic object. If the inserted topic wasnt created, "created" will be true, the object will be created in DB and "topic" receive the topic object
        room=Room.objects.create(host=request.user,topic=topic,name=request.POST.get('name'),description=request.POST.get('description'))
        room.host=request.user#Set the current user as a room host
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):# Update table in DB
    room=Room.objects.get(id=pk)#It returns the row id is iquals to primarykey(pk)
    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here!!</h1>')
    form=RoomForm(instance=room)#form is igual to the form with the info of the row
    if request.method=="POST":#If the method of the request be POST...
        topic_name=request.POST.get('topic')#Get the name inserted in the topic input
        topic, created=Topic.objects.get_or_create(name=topic_name)#If the inserted topic already was created, "created" will be False and "topic" var will receive the topic object. If the inserted topic wasnt created, "created" will be true, the object will be created in DB and "topic" receive the topic object
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')#Redirect the user to the home page
    context={'form':form,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):#Delete data in DB
    room=Room.objects.get(id=pk)
    if request.user!=room.host:#If the user is trying to scess the URL to delete a room that isn't his...
        return HttpResponse('<h1>You are not allowed here!!</h1>')
    if request.method=="POST":#If it be a POST request...
        room.delete()#Delete the room of DB
        return redirect('home')
    context={'obj':room}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def deleteMessage(request,pk):#Delete data in DB
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('<h1>You are not allowed here!!</h1>')
    if request.method=="POST":#If it be a POST request...
        message.delete()#Delete the message of DB
        return redirect('home')
    context={'obj':message}
    return render(request,'base/delete.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)#It gets the user in the database
    rooms=user.room_set.all()#room_set.all() get every data of Room model OF THIS SPECIFIC USER
    roomMessages=user.message_set.all()#message_set.all() get every data of Message model OF THIS SPECIFIC USER
    topics=Topic.objects.all()#It returns every data in topic in DB 
    context={'user':user,'rooms':rooms,'roomMessages':roomMessages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user=request.user#Get the current user
    form=UserForm(instance=user)#form is equal to user form that have the info of current user
    if request.method=="POST":#If the request method is POST
        form=UserForm(request.POST,request.FILES,instance=user)#form will be equal to the new data inserted about the current user
        if form.is_valid():#if the form is valid...
            form.save()#Save the info in DB
            return redirect('home')
    context={'form':form}
    return render(request,'base/update_user.html',context)

def topicsPage(request):
    q=''#It is the "?q=" value of the URL
    if request.GET.get('q')!=None:
        q=request.GET.get('q')
    topics=Topic.objects.filter(Q(name__icontains=q))#It returns the topic searched
    context={'topics':topics}
    return render(request,'base/topics.html',context)

def activitiesPage(request):
    roomMessages=Message.objects.all()#It returns all te rooms in DB
    context={'roomMessages':roomMessages}
    return render(request,'base/activity.html',context)
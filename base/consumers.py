import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Room,Message,User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'#Set the room group name
        self.accept()#It inits the connection(Accepts the connection call)
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.send(text_data=json.dumps({'type':'Conexão foi estabilizada','Message':'Você está conectado!'}))#Send the JSON to client-side(Front End)

    def receive(self, text_data):#It receives message from websocket(It comes to client-side)
        text_data_dict = json.loads(text_data)#It loads the json object in a dicitonary
        room=Room.objects.get(id=text_data_dict['roomPK'])#It returns the row id is iquals to primarykey(pk)
        objectUser=User.objects.get(username=text_data_dict['messageUsername'])#
        roomMessages=room.message_set.all().order_by('id')#message_set.all() get every data of Message model IN THIS SPECIFIC ROOM
        participants=room.participants.all()#It returns every participants IN THIS SPECIFIC ROOM
        message=Message.objects.create(user=objectUser,room=room,body=text_data_dict['message'])#Save the info in the DB
        room.participants.add(objectUser)
        text_data_dict['messageCreated']=str(message.created)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,text_data_dict)

    def chat_message(self, event):#Send data to client-side by Websocket
        self.send(text_data=json.dumps(event))#Send the JSON to client-side(Front End)

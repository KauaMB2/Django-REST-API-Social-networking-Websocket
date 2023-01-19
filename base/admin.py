from django.contrib import admin

# Register your models here.

from .models import Room,Topic,Message,User

admin.site.register(User)#Give to the Amin the possibility to handle User table of database in the website
admin.site.register(Room)#Give to the Admin the possibility to handle Room table of database in the website
admin.site.register(Topic)#Give to the Admin the possibility to handle Topic table of database in the website
admin.site.register(Message)#Give to the Admin the possibility to handle Message table of database in the website


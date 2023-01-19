from django.urls import path
from . import views

urlpatterns=[
	path('',views.getRoutes),
	path('rooms/',views.getRooms),
	path('getRoom/<str:pk>/',views.getRoom),
	path('putRoom/<str:pk>/<str:username>/<str:password>/',views.putRoom),
	path('deleteRoom/<str:pk>/<str:username>/<str:password>/',views.deleteRoom),
	path('postRoom/<str:username>/<str:password>/',views.postRoom),
]
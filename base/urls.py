from django.urls import path
from . import views

urlpatterns=[
	path('login/',views.loginPage,name="login"),
	path('logout/',views.logoutPage,name="logout"),
	path('register/',views.registerPage,name="register"),
	path('',views.home,name="home"),
	path('home/',views.home,name="home"),
	path('room/<str:pk>/',views.room,name="room"),#<str:pk> => Dynamic url route
	path('create-room',views.createRoom,name="create-room"),
	path('update-room/<str:pk>/',views.updateRoom,name="update-room"),#<str:pk> => Dynamic url route
	path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),#<str:pk> => Dynamic url route
	path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),#<str:pk> => Dynamic url route
	path('profile/<str:pk>/',views.userProfile,name="user-profile"),#<str:pk> => Dynamic url route
	path('update-user/',views.updateUser,name="update-user"),
	path('topics/',views.topicsPage,name="topics"),
	path('activities/',views.activitiesPage,name="activities"),
]
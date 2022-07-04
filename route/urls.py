from django import views
from django.urls import URLPattern, path 
from . import views



urlpatterns = [
    path('',views.home , name='home'),
    path('login/',views.loginPage , name='login'),
     path('logout/',views.logoutPage , name='logout'),
     path('profile/', views.profilePage, name='profile'),
      path('register/', views.addUser, name='register'),
       path('result/', views.tabuResult, name='tabuResult')

]


from django.contrib import admin
from django.urls import path
from user_auths import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    path("edit_profile/",views.edit_profile,name="edit_profile"),



        # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('login/', views.login_view, name="login"),
 
    
    
]
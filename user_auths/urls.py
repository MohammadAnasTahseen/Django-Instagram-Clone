from django.contrib import admin
from django.urls import path
from user_auths import views
urlpatterns = [
    path("edit_profile/",views.edit_profile,name="edit_profile"),

    
    
]
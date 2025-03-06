from django.contrib import admin
from django.urls import path
from confabulation import views
urlpatterns = [
    path('', views.inbox, name="message"),
    path('direct/<username>', views.Directs, name="directs"),
    path('send/', views.SendDirect, name="send-directs"),
    path('search/', views.UserSearch, name="search-users"),
    path('new/<username>', views.NewConversation, name="conversation"),
]
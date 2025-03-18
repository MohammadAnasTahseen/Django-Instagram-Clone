from django.contrib import admin
from django.urls import path
from confabulation import views
urlpatterns = [
    path('', views.inbox, name="message"),
    path('direct/<username>', views.Directs, name="directs"),
    path('send/', views.SendDirect, name="send-directs"),

    path('searchpage/', views.UserSearch_page, name="search-users"),

    path('search_func/', views.UserSearch, name="search_users_func"),


    path('new/<username>', views.NewConfabulation, name="NewConfabulation"),
]
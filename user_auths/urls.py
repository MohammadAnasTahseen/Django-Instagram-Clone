from django.contrib import admin
from django.urls import path
from user_auths import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    path("edit_profile/",views.edit_profile,name="edit_profile"),



        # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="Auth_templates/login.html", redirect_authenticated_user=True), name='sign_in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="Auth_templates/sign_out.html"), name='sign_out'), 

    
    
]
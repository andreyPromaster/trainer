from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path ('login/', auth_views.LoginView.as_view(template_name = "account/registration/login.html"), name = 'user login'),
    path ('register/',views.register, name = 'registrate'),
    path ('logout/', views.logout_view, name = 'user_logout'),
    path ('edit_profile/', views.edit_profile, name = 'edit_profile'),
]


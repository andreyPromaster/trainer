from django.urls import path
from . import views

urlpatterns = [
    path ('login/', views.user_login, name = 'user login'),
    path ('register/',views.register, name = 'registrate'),
    path ('logout/', views.logout_view, name = 'user_logout'),
]


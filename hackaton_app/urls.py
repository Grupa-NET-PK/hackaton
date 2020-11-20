from django.urls import path
from . import views
from .views import register, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name='hackaton_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='hackaton_app/logout.html'), name='logout'),
]

from django.template.defaulttags import url
from django.urls import path, include
from . import views
from .views import Mylogin, Mylogout, register, profile_page, editprofile, home_page, activate

urlpatterns = [
    path('', register,name="index"),
    path('home/', home_page, name="index"),
    path('profile/<str:username>', profile_page, name='profile'),
    path('editprofile/<int:id>', editprofile, name='editprofile'),
    path("register/",register,name="register"),
    path("login/", Mylogin, name='login'),
    path("logout/", Mylogout, name="logout"),
    #path("activate/", activate)
    #path('activate/<uidb64>/<token>',activate),
]
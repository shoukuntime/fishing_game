"""
URL configuration for game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register,name="register"),
    path('login/', views.user_login,name="login"),
    path('profile/', views.user_profile,name="profile"),
    path('logout/', views.user_logout,name="logout"),
    path('', views.user_story,name="story"),
    path('text/', views.user_text,name="text"),
    path('rank/', views.user_rank,name="rank"),
]

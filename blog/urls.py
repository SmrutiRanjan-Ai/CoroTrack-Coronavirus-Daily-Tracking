from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name="starting-page"),
    path("register/", views.register, name="register"),
    path("login/",views.login, name="login"),
    path("logout",views.logout,name="logout"),
    path("search",views.search,name="search")
]

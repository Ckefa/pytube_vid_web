from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
(path('vidplay/', views.vidplay, name="vidplay")),
(path('', views.main_page_view, name="main_page_view")),
(path("signup/", views.signup, name="signup")),
(path("login/", views.signin, name='login')),
(path('logout/', views.signout, name='logout')),

] 
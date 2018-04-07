from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='LandingPage'),
    path('home/', views.HomePage.as_view(), name='HomePage'),
    path('home/location', views.LocBasedHomePage.as_view(), name='LocBasedHomePage')
]
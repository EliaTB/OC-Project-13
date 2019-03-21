from django.urls import path
from . import views

app_name = "resv"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('deals/', views.deals, name='deals'),
]
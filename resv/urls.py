from django.urls import path
from .views import DealListView, DealDetailView, DealCreateView
from . import views

app_name = "resv"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('deals/', DealListView.as_view(), name='deals'),
    path('deals/<int:pk>/', DealDetailView.as_view(), name='deal-detail'),
    path('deals/new/', DealCreateView.as_view(), name='deal-create'),
]
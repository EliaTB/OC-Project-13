from django.urls import path
from .views import ( 
    DealListView,
    CategoryListView,
    DealCreateView,
    DealUpdateView,
    DealDeleteView,
    DealSearchView
)
from . import views

app_name = "deals"

urlpatterns = [
    path('', views.home, name='home'),
    path('deals/', DealListView.as_view(), name='deals'),
    path('deals/search/', DealSearchView.as_view(), name='deals-search'),
    path('deals/category/<category>', CategoryListView.as_view(), name='deals-category'),
    path('deals/new/', DealCreateView.as_view(), name='deal-create'),
    path('deals/<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    path('deals/<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('deals/<int:deal_id>', views.deal_detail, name='deal-detail'),
]
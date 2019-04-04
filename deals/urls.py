from django.urls import path
from .views import ( 
    DealListView,
    CategoryListView,
    DealDetailView,
    DealCreateView,
    DealUpdateView,
    DealDeleteView,
    DealSearchView
)
from . import views

app_name = "deals"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('deals/', DealListView.as_view(), name='deals'),
    path('deals/search/', DealSearchView.as_view(), name='deals-search'),
    path('deals/category/<category>', CategoryListView.as_view(), name='deals-category'),
    path('deals/<int:pk>/', DealDetailView.as_view(), name='deal-detail'),
    path('deals/new/', DealCreateView.as_view(), name='deal-create'),
    path('deals/<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    path('deals/<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('deals/upload/<int:deal_id>', views.upload_img, name='uploadimg'),
]
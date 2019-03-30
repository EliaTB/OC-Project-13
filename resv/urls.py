from django.urls import path
from .views import ( 
    DealListView, 
    DealDetailView, 
    DealCreateView, 
    DealUpdateView, 
    DealDeleteView, 
    ReservationCreateView,
    ReservationListView,
    ReservationReqListView,
)
from . import views

app_name = "resv"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('deals/', DealListView.as_view(), name='deals'),
    path('deals/<int:pk>/', DealDetailView.as_view(), name='deal-detail'),
    path('deals/new/', DealCreateView.as_view(), name='deal-create'),
    path('deals/<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    path('deals/<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    path('deals/reservation/create/<int:pk>', ReservationCreateView.as_view(), name='resv-create'),
    path('reservations/', ReservationListView.as_view(), name='resv-list'),
    path('reservations/requests', ReservationReqListView.as_view(), name='resvreq-list'),
    path('accept-reservation/<int:reservation_id>', views.accept_reservation, name='accept_reservation'),
    path('refuse-reservation/<int:reservation_id>', views.refuse_reservation, name='refuse_reservation')
]
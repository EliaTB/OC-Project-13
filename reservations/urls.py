from django.urls import path
from .views import ( 
    ReservationCreateView,
    ReservationListView,
    ReservationReqListView,
)
from . import views

app_name = "reservations"

urlpatterns = [
    path('', ReservationListView.as_view(), name='resv-list'),
    path('create/<int:pk>', ReservationCreateView.as_view(), name='resv-create'),
    path('requests/', ReservationReqListView.as_view(), name='resvreq-list'),
    path('accept-reservation/<int:reservation_id>', views.accept_reservation, name='accept_reservation'),
    path('refuse-reservation/<int:reservation_id>', views.refuse_reservation, name='refuse_reservation')
]
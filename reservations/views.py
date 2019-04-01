from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    success_url = '/deals'
    fields = ['checkin', 'checkout', 'adult_nb', 'children_nb']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.deal_id = self.kwargs['pk']
        form.instance.status = Reservation.REQUESTED
        return super().form_valid(form)


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReservationReqListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations_req.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return self.model.objects.filter(deal__author=self.request.user)


def accept_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 1
    reservation.save()
    messages.success(request, 'You accepted the reservation')
    return redirect(request.META.get('HTTP_REFERER'))


def refuse_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 2
    reservation.save()
    messages.warning(request, 'You refused the reservation')
    return redirect(request.META.get('HTTP_REFERER'))
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.http import HttpResponseForbidden
from .models import Reservation
from .forms import ReservationForm


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    success_url = '/reservations'
    form_class = ReservationForm

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


class RequestListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/requests.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return self.model.objects.filter(deal__author=self.request.user)


@login_required
def reservation_accept_confirm(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.user != reservation.deal.author:
        return HttpResponseForbidden()
    return render(request, 'reservations/reservation_accept_confirm.html', {'reservation':reservation})  


@login_required
def reservation_refuse_confirm(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.user != reservation.deal.author:
        return HttpResponseForbidden()
    return render(request, 'reservations/reservation_refuse_confirm.html', {'reservation':reservation})  


def accept_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 1
    reservation.save()
    messages.success(request, 'You accepted the reservation')
    return redirect('/reservations/requests/')


def refuse_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 2
    reservation.save()
    messages.success(request, 'You refused the reservation')
    return redirect('/reservations/requests/')
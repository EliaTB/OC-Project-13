from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Deal, Reservation


def home(request):
    return render(request, 'resv/home.html')


def about(request):
    return render(request, 'resv/about.html')


class DealListView(ListView):
    model = Deal
    template_name = 'resv/deals.html'
    context_object_name = 'deals'
    ordering = ['-date_posted']


class DealDetailView(DetailView):
    model = Deal


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    fields = ['name', 'category', 'short_description', 'content', 'location',  'thumbnail']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deal
    fields = ['name', 'category', 'short_description', 'content', 'location',  'thumbnail']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        deal = self.get_object()
        if self.request.user == deal.author:
            return True
        return False


class DealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Deal
    success_url = '/deals'

    def test_func(self):
        deal = self.get_object()
        if self.request.user == deal.author:
            return True
        return False


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    success_url = '/deals'
    fields = ['checkin', 'checkout']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.deal_id = self.kwargs['pk']
        form.instance.status = Reservation.REQUESTED
        return super().form_valid(form)


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'resv/reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReservationReqListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'resv/reservations_req.html'
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
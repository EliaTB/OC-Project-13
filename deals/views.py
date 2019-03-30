from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Deal


def home(request):
    return render(request, 'deals/home.html')


def about(request):
    return render(request, 'deals/about.html')


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deals.html'
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
        return FalseS
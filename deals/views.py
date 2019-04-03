from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Deal
from .forms import DealForm, DealImagesForm
import json


def home(request):
    return render(request, 'deals/home.html')


def about(request):
    return render(request, 'deals/about.html')


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deals.html'
    context_object_name = 'deals'
    ordering = ['-date_posted']


class DealCategoryListView(ListView):
    model = Deal
    template_name = 'deals/deals.html'
    context_object_name = 'deals'
    ordering = ['-date_posted']

    def get_queryset(self):
        self.category = self.kwargs['category']
        return Deal.objects.filter(category=self.category)


class DealSearchView(ListView):
    template_name = 'deals/deals.html'
    model = Deal
    context_object_name = 'deals'

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = self.model.objects.filter(location__icontains = query)
        return object_list


def autocomplete(request):

    if request.is_ajax():
        query = request.GET.get('term', '')
        deals = Deal.objects.filter(location__icontains = query)
        results = []
        for p in deals:
            deal_dict = {}
            deal_dict = p.location
            results.append(deal_dict)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')


class DealDetailView(DetailView):
    model = Deal


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deal
    fields = DealForm

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
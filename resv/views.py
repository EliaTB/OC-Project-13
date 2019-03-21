from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Deal


def home(request):
    return render(request, 'resv/home.html')


def about(request):
    return render(request, 'resv/about.html')


def deals(request):
	context = {
	    'deals': Deal.objects.all()
	}
	return render(request, 'resv/deals.html', context)


class DealListView(ListView):
    model = Deal
    template_name = 'resv/deals.html'
    context_object_name = 'deals'
    ordering = ['-date_posted']


class DealDetailView(DetailView):
    model = Deal


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    fields = ['name', 'short_description', 'content', 'location',  'picture']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
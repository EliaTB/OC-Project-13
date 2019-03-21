from django.shortcuts import render, redirect
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
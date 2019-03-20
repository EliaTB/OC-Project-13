from django.shortcuts import render, redirect


def home(request):
    return render(request, 'resv/home.html')


def about(request):
    return render(request, 'resv/about.html')

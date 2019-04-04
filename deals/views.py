from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Deal, DealImages
from .forms import DealForm, DealImagesForm
import json


def home(request):
    return render(request, 'deals/home.html')


def about(request):
    return render(request, 'deals/about.html')


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


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deals.html'
    context_object_name = 'deals'
    ordering = ['-date_posted']


class CategoryListView(ListView):
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


# class DealDetailView(DetailView):
#     model = Deal


def deal_detail(request, deal_id):
    ImageFormSet = modelformset_factory(DealImages,
                                        form=DealImagesForm)
   
    deal = Deal.objects.get(id=deal_id)

    if request.method == 'POST':
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if formset.is_valid():
            for form in formset.cleaned_data:
                image = form['image']
                photo = DealImages(deal=deal, image=image)
                photo.save()  

            messages.success(request, f'Your image has been uploaded!')
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        formset = ImageFormSet(queryset=DealImages.objects.none())

    context = {
    'i_form': formset,
    'object': deal,
    }

    return render(request, 'deals/deal_detail.html', context) 
        

class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deal
    form_class = DealForm

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
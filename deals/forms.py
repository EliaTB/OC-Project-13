from django import forms
from .models import Deal, DealImages


class DealForm(forms.ModelForm):
	class Meta:
		model = Deal
		fields = ['name', 'category', 'short_description', 'content', 'location',  'thumbnail']


class DealImagesForm(forms.ModelForm):
	class Meta:
		model = DealImages
		fields = ['image']
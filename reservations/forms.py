from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['checkin', 'checkout', 'adult_nb', 'children_nb']
		widgets = {
		    'checkin': forms.DateTimeInput(attrs={'class': 'checkin-picker'}),
		    'checkout': forms.DateTimeInput(attrs={'class': 'checkout-picker'})
		}

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

	def __init__(self, *args, **kwargs):
		super(ReservationForm, self).__init__(*args, **kwargs)
		self.fields['adult_nb'].label = 'Number of adults'
		self.fields['children_nb'].label = 'Number of children'

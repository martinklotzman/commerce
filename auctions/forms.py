from django import forms
from .models import Listing, Category, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(choices=[(category.id, category.name) for category in Category.objects.all()])
        }
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01', 'class': 'form-control'})
        }
        labels = {
            'amount': 'Your Bid ($)'
        }

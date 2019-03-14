from django import forms

from dutch.models import DutchBid

class DutchBidForm(forms.ModelForm):
    class Meta:
        model = DutchBid
        template_name = 'dutch/bid.html'
        fields = ['bid_price',]
# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from notifications.signals import notify

from . import forms, models
from dutch.models import DutchBid, DutchAuction


def submit_bid(request):
    
    user = request.user
    dutch = DutchAuction.objects.get(pk=1)
    form = forms.DutchBidForm(request.POST or None)
    
    if request.POST:
        
        if form.is_valid():
            form.instance.bidder = user
            # form.instance.price = form.instance.unit_price
        
            if form.instance.bid_price > dutch.lead_bid_price:
                dutch.bidder = user
                dutch.lead_bid_price = form.instance.bid_price
               
                form.save()
                dutch.save()
            
            else:
                form.add_error('price', "You must submit a bid higher than the current bid!")

    context = {'form': form, 'page_title': f'Bid on equity in AA', 'current':dutch.lead_bid_price}
    
    return render(request, 'dutch/bid.html', context=context)


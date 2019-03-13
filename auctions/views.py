from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from notifications.signals import notify

from . import forms, models
from auctions.models import Auction, Bid, Transaction

UNDERLYING = ('LICENSE', 'PATENT', 'PLANT')

def index(request):
    return render(request, 'auctions/index.html')

def auctions(request):
    lots = Auction.objects.filter(status__exact='OPEN').filter(asset_class__exact=request.GET.get('asset'))
    return render(request, 'auctions/auctions.html', context= {'listings': lots})

def new_auction(request):
    '''Simple form for adding a new auctions'''

    a_class = request.GET.get('asset')
    deriv = True if a_class in UNDERLYING else False
    if request.POST:
        form = forms.NewAuctionForm(request.POST) if not deriv else forms.NewDerivativeAuctionForm(request.POST)
        if form.is_valid():
            if not deriv:
                form.instance.underlying_asset = a_class
            form.instance.asset_class = a_class
            form.instance.seller = request.user
            form.instance.high_bid = form.instance.unit_price
      
            form.save()

            return redirect(f'/auctions/listings?asset={a_class}')
    
    else:
        form = forms.NewAuctionForm(request.POST) if not deriv else forms.NewDerivativeAuctionForm(request.POST)

    return render(request, 'auctions/new.html',context={'form': form, 'page_title': 'New auction'})

def submit_bid(request):
    
    user = request.user
    auction_pk = request.GET.get('auction')
    auction = Auction.objects.get(pk=auction_pk)
    form = forms.AuctionBidForm(request.POST or None, initial={'auction': auction_pk, 'price': auction.high_bid})
    
    if request.POST:
        
        if form.is_valid():
            form.instance.bidder = user
            # form.instance.price = form.instance.unit_price
            form.instance.auction = auction

            if form.instance.price > auction.high_bid:
                auction.high_bid = form.instance.price
                auction.high_bid_id = form.instance.id

                if auction.high_bid > auction.buy_it_now_price:
                    auction.status = 'HELD'

                    transaction = Transaction.objects.create(
                        auction=auction, buyer=user,
                        seller=auction.seller, shipping=form.instance.shipping,
                        )


                form.save()
                auction.save()
                notify.send(user, recipient=user, verb="Your bid was accepted!")

                return redirect(f'/auctions/listings?asset={auction.asset_class}')
            
            else:
                form.add_error('price', "You must submit a bid higher than the current bid!")

    context = {'form': form, 'page_title': f'Bid on {auction_pk}', 'auction': auction_pk,}
    
    return render(request, 'auctions/bid.html',context=context)



def submit_buynow(request):
    auction_pk = request.GET.get('auction')
    auction = Auction.objects.get(pk=auction_pk)
    form = forms.AuctionBuyNowForm(request.POST or None, initial={'auction': auction_pk, 'price': auction.buy_it_now_price})

    if request.POST:
        
        if form.is_valid():
            form.instance.bidder = request.user
            form.instance.price = auction.buy_it_now_price
            form.instance.auction = auction

            auction.status = 'HELD'

            form.save()
            auction.save()
            transaction = Transaction.objects.create(
                        auction=auction, buyer=request.user,
                        seller=auction.seller, shipping=form.instance.shipping,
                        )


            return redirect(f'/auctions/listings?asset={auction.asset_class}')
            

    context = {'form': form, 'page_title': f'Bid on {auction_pk}', 'auction': auction_pk,}
    
    return render(request, 'auctions/buynow.html',context=context)


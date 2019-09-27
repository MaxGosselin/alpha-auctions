from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from notifications.signals import notify

from . import forms, models, emails
from auctions.models import Auction, Bid, Transaction



DERIVS = ('LICENSE', 'PATENT', 'PLANT')

def index(request):
    return render(request, 'auctions/index.html')

def auctions(request):
    
    a_class = request.GET.get('asset')
    lots = Auction.objects.filter(status__exact='OPEN').filter(asset_class__exact=a_class).order_by('high_bid')
    deriv = True if a_class in DERIVS else False
    
    form = forms.NewAuctionForm(request.POST or None) if not deriv else forms.NewDerivativeAuctionForm(request.POST)
    if form.is_valid():
        if not deriv:
            form.instance.underlying_asset = a_class
        form.instance.asset_class = a_class
        form.instance.seller = request.user
        form.instance.high_bid = form.instance.unit_price
    
        form.save()
        send_mail('Auction posted!', emails.AUCTION_POSTED, 'auctioneer@mg.maxgosselin.com', [request.user.email,])


    context = {'asset': a_class, 'form':form, 'page_title': f"{a_class} Auctions", 'listings': lots}
    
    return render(request, 'auctions/auctions.html', context=context)

# def new_auction(request):
#     '''Simple form for adding a new auctions'''

#     a_class = request.GET.get('asset')
#     deriv = True if a_class in DERIVS else False
#     if request.POST:
#         form = forms.NewAuctionForm(request.POST) if not deriv else forms.NewDerivativeAuctionForm(request.POST)
#         if form.is_valid():
#             if not deriv:
#                 form.instance.underlying_asset = a_class
#             form.instance.asset_class = a_class
#             form.instance.seller = request.user
#             form.instance.high_bid = form.instance.unit_price
     
#             form.save()
#             return redirect(f'/auctions/listings?asset={a_class}')
    
#     else:
#         form = forms.NewAuctionForm(request.POST) if not deriv else forms.NewDerivativeAuctionForm(request.POST)

#     return render(request, 'auctions/new.html',context={'form': form, 'page_title': f"{a_class} Auctions"})

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
                auction.high_bid_id = user.id

                if auction.high_bid > auction.buy_it_now_price:
                    auction.status = 'HELD'

                    transaction = Transaction.objects.create(
                        t_auction=auction, t_buyer=request.user,
                        t_seller=auction.seller, shipping=form.instance.shipping,
                        t_price=auction.high_bid,
                        )
                    emails.transaction_notify(transaction)

                form.save()
                auction.save()
            

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
                        t_auction=auction, t_buyer=request.user,
                        t_seller=auction.seller, shipping=form.instance.shipping,
                        t_price=auction.buy_it_now_price,
                        )
            emails.transaction_notify(transaction)

            return redirect(f'/auctions/listings?asset={auction.asset_class}')
            

    context = {'form': form, 'page_title': f'Bid on {auction_pk}', 'auction': auction_pk,}
    
    return render(request, 'auctions/buynow.html',context=context)


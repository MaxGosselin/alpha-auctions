from django import forms

from auctions.models import Auction, Bid, Transaction

class NewAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        template_name = 'auctions/new.html'
        fields = ['grade', 'region', 'quantity',
                  'unit_price', 'buy_it_now_price',]
        
class NewDerivativeAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        template_name = 'auctions/new.html'
        fields = ['underlying_asset', 'unit_price', 'buy_it_now_price','grade', 'region',]

    def __init__(self, *args, **kwargs):
        super(NewDerivativeAuctionForm, self).__init__(*args, **kwargs)
        self.fields['grade'].required = False
        self.fields['region'].required = False

class AuctionBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        template_name = 'auctions/bid.html'
        fields = ['price', 'shipping',]
        
class AuctionBuyNowForm(forms.ModelForm):
    class Meta:
        model = Bid
        template_name = 'auctions/bid.html'
        fields = ['shipping',]
        
    # def clean(self):
    #     cd = self.cleaned_data
    #     if cd.get('price') <= Auction.objects.get(pk=self.fields['auction']).high_bid:
    #         self.add_error('price', "You must submit a bid higher than the current bid!")
    #     return cd
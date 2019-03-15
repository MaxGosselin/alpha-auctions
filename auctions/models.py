from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.template.defaultfilters import slugify

from homepage.models import User
from auctions.auction_timer import period_end

ASSETS = (('X', 'X'),
          ('Y', 'Y'),
          ('PATENT', 'Patent'),
          ('LICENSE', 'License'),
          ('PLANT', 'Plant'),
)

UNDERLYING_ASSETS = (
          ('X', 'X'),
          ('Y', 'Y'),
)

REGIONS = (('West', 'Western Canada'),
          ('Central', 'Central Canada'),
          ('East', 'Eastern Canada'),
          ('Home', 'Home Office'),
)

SHIPPING = (
          ('Ground', 'Ground Frieght'),
          ('Air', 'Air Frieght'),
)

STATUSES = (('OPEN', 'Open'),
          ('CLOSED', 'Closed'),
          ('HELD', 'Held'),
)

T_STATUSES = (
          ('Processing', 'Transaction in Progress'),
          ('Cleared', 'Transaction Cleared'),
)



class Auction(models.Model):

    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="seller", blank=True)

    asset_class = models.CharField(max_length=10, choices=ASSETS, default='X')
    underlying_asset = models.CharField(max_length=10, choices=UNDERLYING_ASSETS, default='X')

    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=0)
    region = models.CharField(max_length=10, choices=REGIONS, default='H')
    
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000000)], default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=1, default=25.00)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=1, default=25.00)

    # bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bidder", blank=True)
    high_bid = models.DecimalField(max_digits=10, decimal_places=1, default=25.00)
    high_bid_id = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)

    closing_date = models.DateTimeField(default=period_end, blank=True)
    opening_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=10, default="OPEN")

    views = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Auctions'

    def __str__(self):
        return f"An {self.asset_class} auction by {self.seller}! Current high bid: {self.high_bid} | Auction ID: {self.id}"
    
    def get_absolute_url(self):
        return reverse('listings')

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=1, default=25.00)
    shipping = models.CharField(max_length=10, choices=SHIPPING, default="Ground")

    class Meta:
        verbose_name_plural = 'Bids'

    def __str__(self):
        return f"Bid of {self.price} on Auction: {self.auction}) | Bid ID: {self.id}"
    


class Transaction(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="t_buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="t_seller")
    t_status = models.CharField(max_length=10, choices=T_STATUSES, default="Processing")

    shipping = models.CharField(max_length=10, default="ground")

    class Meta:
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.t_status} Transaction between {self.buyer} and {self.seller}) | Transaction ID: {self.id}; Auction: {self.auction}"
    


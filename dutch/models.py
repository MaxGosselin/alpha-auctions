from django.db import models
from homepage.models import User
# Create your models here.
STARTING_BID = 2.50
STATUSES = (('OPEN', 'Open'),
          ('CLOSED', 'Closed'),
)
class DutchBid(models.Model):

    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)

    class Meta:
        verbose_name_plural = 'Dutch Bids'

    def __str__(self):
        return f"Bid of {self.bid_price} by {self.bidder}"

class DutchAuction(models.Model):

    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    lead_bid_price = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)

    class Meta:
        verbose_name_plural = 'The Dutch Auction'

    def __str__(self):
        return f"The real auction"


from django.contrib import admin
from auctions.models import Auction, Bid, Transaction
# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Transaction)
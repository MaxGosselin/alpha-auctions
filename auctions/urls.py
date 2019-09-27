from django.conf.urls import url
from . import views
from django.urls import include

urlpatterns = [
    url(r"^listings", views.auctions, name="listings"),
    # url(r"^new", views.new_auction, name="new_auction"),
    url(r"^bid", views.submit_bid, name="submit_bid "),
    url(r"^buynow", views.submit_buynow, name="submit_buynow"),
    url(r"^$", views.index, name="index"),
    ]
    
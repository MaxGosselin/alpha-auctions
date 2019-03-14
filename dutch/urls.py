from django.conf.urls import url
from . import views
from django.urls import include

urlpatterns = [

    url(r"^$", views.submit_bid, name="submit_bid "),

    ]
    
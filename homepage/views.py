from django.shortcuts import render
# from dutch.models import DutchAuction

def home(request):

    context = {}

    return render(request, 'homepage/home.html', context=context)

def guide(request):
    return render(request, 'accounts/profile.html')

def profile(request):
    return render(request, 'accounts/profile.html')
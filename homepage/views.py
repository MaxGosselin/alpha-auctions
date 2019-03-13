from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')

def profile(request):
    return render(request, 'accounts/profile.html')
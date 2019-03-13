from django.conf.urls import url
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from . import views, forms


urlpatterns = [
    url(r"^accounts/profile/$", views.profile, name="profile"),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            form_class=forms.UserForm
        ),
        name='django_registration_register',
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r"^$", views.home, name="home"),
    ]

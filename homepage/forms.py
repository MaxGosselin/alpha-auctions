from django_registration.forms import RegistrationFormTermsOfService

from .models import User

class UserForm(RegistrationFormTermsOfService):
    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
        
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2', 'team', 'referral_code', 'tos']
        # print(fields)

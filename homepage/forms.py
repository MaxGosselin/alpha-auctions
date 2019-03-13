from django_registration.forms import RegistrationFormTermsOfService

from .models import User

class UserForm(RegistrationFormTermsOfService):
    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
        
        fields = ['username', 'name', 'email', 'password1', 'password2', 'team', 'tos']
        # print(fields)

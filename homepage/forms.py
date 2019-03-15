from django_registration.forms import RegistrationFormTermsOfService

from .models import User

class UserForm(RegistrationFormTermsOfService):
    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
        
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2', 'team', 'referral_code', 'tos']
        # print(fields)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['referral_code'].required = False
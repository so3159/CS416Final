from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.widgets import EmailInput
from accounts.models import Profile



def ForbiddenUsers(value):
	forbbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'root', 'administrator'
	'email', 'join', 'sql', 'insert', 'db', 'static', 'python', 'delete', 'TABLE', 'insert']
	if value.lower() in forbbidden_users:
		raise ValidationError('Invalid name for user, this is a reserved word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an invalid user, do not use these chars: @, - , +')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this this username already exists.')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')


# This form is not currently used, but I included in case you need to design a custom UserRegistrationForm where
# you can ask the user to enter email and password instead of password and username to register your site
class UserRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=False, label='Email')
    first_name= forms.CharField(widget=forms.TextInput(),  max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(),  max_length=50, required=False)
    

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsers)
        self.fields['username'].validators.append(InvalidUser)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        super(UserRegistrationForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match. Try again'])
        return self.cleaned_data




class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    username = forms.CharField(widget=forms.TextInput(), max_length=50, required =False)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']
    
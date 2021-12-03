from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm



# Create your views here.

def register_view(request):
    
    if request.method == 'POST':
        
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # if you want to login the user directly after registration, use the following three lines,
            # which login the user and redirect to index
            user = form.save()
            login(request, user)
            return redirect('index')
            # if you do want to login the user directly after registration, comment out the three lines above,
            # save the form data and then redirect the user to login page so that after registration the user can enter the credentials
            # form.save()
            # return redirect('login')
    else:
        #create empty Instance of Djangos Form to generate html
        form= UserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})
            
        
def logout_view(request):
    #Method to logout
    logout(request)
    #redirect the user to the index page after logout
    return redirect('index')

def login_view(request):
    # this function authenticates the user based on username and password
    # AuthenticationForm is a form for logging a user in.
    # if the request method is a post
    if request.method == 'POST':
        # Plug the request.post in AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the user info from the form data and login the user
            user = form.get_user()
            login(request, user)
            # redirect the user to index page
            return redirect('index')
    else:
        # Create an empty instance of Django's AuthenticationForm to generate the necessary html on the template.
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#import User From Auth
from django.contrib.auth.models import User
from accounts.models  import Profile
from movie.models import Movie, List
from accounts.forms import EditProfileForm, UserRegistrationForm


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegistrationForm
from django.contrib import messages
#messages.info messages.warning messages.success


# Create your views here.

def register_view(request):
    
    if request.method == 'POST':
        
        
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            # if you want to login the user directly after registration, use the following three lines,
            # which login the user and redirect to index
            print(user)
            login(request, user)
            print(user.username)
            return redirect('search')
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
    messages.warning(request, 'Successfully Logged Out!')

    #redirect the user to the index page after logout
    return redirect('index')

def login_view(request):
    # this function authenticates the user based on username and password
    # AuthenticationForm is a form for logging a user in.
    # if the request method is a post
    if request.method == 'POST':
        # Plug the request.post in AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            print('also here')
            # get the user info from the form data and login the user
            user = form.get_user()
            messages.success(request, 'Successfully Logged In!')

            login(request, user)
            # redirect the user to index page
            return redirect('search')
        else:
            return render(request,'accounts/login.html', {'form':form})
    
    form = AuthenticationForm()
    messages.warning(request, 'Failed To Log In!')

    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='index')
def view_profile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    lists = List.objects.filter(profile=profile).order_by('id').reverse()

    
    context = {
        
        'profile' : profile,
        'lists':lists
        
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='index')
def view_list(request):
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    lists = List.objects.filter(profile=profile).order_by('id').reverse()
    
    
    
    if request.method == 'POST':
        list_name = request.POST['list_name']
        list=List.objects.filter(profile=profile).get(name= list_name)
        movies = list.movies.all()
        
        context = {
            
            'list' : movies,
            'profile':profile,
            'lists':lists,
        }
        return render(request, 'accounts/profile.html',context)

@login_required(login_url='index')
def edit_profile(request): 
    
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.user.username = form.cleaned_data.get('username')
            print(profile.user.username)
            #profile.user.save()
            profile.save()
            print(authenticate(user))
            profile.user.save()
            messages.success(request, 'Successfully Edited Your Profile!')

            context ={
                'profile':profile,
                
                'form':form
            }
            return render(request,'accounts/edit_profile.html', context)
        
    
    else:
        form = EditProfileForm()
        #print(profile.user.username)
        context= {
            'form': form,
            'profile': profile,
            
        }
        
        return render(request, 'accounts/edit_profile.html', context)
    
def index(request):
    return render(request, 'accounts/index4.html')


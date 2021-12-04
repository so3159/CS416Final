from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from movie.models import Movie

import requests
# Create your views here.
@login_required(login_url='login')
def search(request):
    
    return render(request, 'search.html')

@login_required(login_url='login')
def results(request):
    
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        
        API_KEY= "k_tx163xr6"
        
        url = f'https://imdb-api.com/en/API/SearchMovie/{API_KEY}/{search_term}'
        
        headers= {
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.get(url,headers=headers)
        data= response.json()
        total_results = data['results']
        print(total_results)
        
        return render(request,'results.html',{
            'results':total_results,
        })
    
    else:
        return render(request, 'index3.html')
    
def movieDetails(request, id):
    id = id
    API_KEY= "k_tx163xr6"
        
    url = f'https://imdb-api.com/en/API/Title/{API_KEY}/{id}/FullActor,Ratings,Wikipedia,'
        
    headers= {
        "Authorization": f"Bearer {API_KEY}"
    }
        
    response = requests.get(url,headers=headers)
    data = response.json()
    return render(request, 'index3.html' ,{'data' : data})
    
    
    
def addMoviesToWatched(request,imbd_id):
    id = imbd_id
    API_KEY= "k_tx163xr6"
        
    url = f'https://imdb-api.com/en/API/Title/{API_KEY}/{id}/FullActor,Ratings,Wikipedia,'
        
    headers= {
        "Authorization": f"Bearer {API_KEY}"
    }
        
    response = requests.get(url,headers=headers)
    data = response.json()
    
    title = data['title']
    year = data['year']
    runtime= data['rurntimeStr']
    rated = data['imDbRating']
    
    
    movie = Movie.objects.create(id = imbd_id, title = title, year = year, runtime=Runtime)
    user = request.user
    profile = Profile.objects.get
    
    profile.watched.add(movie)
    print("added" + movie)
    return redirect(home)
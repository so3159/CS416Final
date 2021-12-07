from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from movie.forms import ListForm

from accounts.models import Profile
from movie.models import Movie, List

from django.db.models import Count

import requests
# Create your views here.
@login_required(login_url='login')
def search(request):
    
    lists = List.objects.all().order_by('id').reverse()
    
    return render(request, 'search.html',{'lists':lists})

@login_required(login_url='login')
def results(request):
    
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        listname= request.POST.get('list_name')
        print(listname)
        
        lists = List.objects.all().order_by('id').reverse()
        
        API_KEY= "k_tx163xr6"
        
        url = f'https://imdb-api.com/en/API/SearchMovie/{API_KEY}/{search_term}'
        
        headers= {
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.get(url,headers=headers)
        data= response.json()
        total_results = data['results']
        #print(total_results)
        #Save All Movies Into Database Here? NOt enough data
        
        return render(request,'search.html',{
            'search_term': search_term,
            'results':total_results,
            'lists': lists,
            'list_name':listname
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
    
    

def addListName(request):
    form = ListForm(request.POST or None)
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    lists = List.objects.all().order_by('id').reverse()
    
    #print(lists)
    
    if request.method == "POST":
        if form.is_valid():
            
            form.save()
            
            context ={
                'lists' :lists,
                'profile':profile,
                'form': form
            }
            #print(form.data.name)
            return render(request,'search.html', context)
    
    context={ 
             'form': form
             
             }
    return render(request, 'makeList.html', context)
    
        



def addMoviesToList(request):
    
    if request.method == "POST":
        
        movies = request.POST.getlist('movies')
        list_name = request.POST.get('list_name')
        list = List.objects.get(name=list_name)
        #print(list)
        
        searchTerm = request.POST.get('search_term')
        #print(f'{movies} + {list} + {searchTerm}')
        
        for x in movies:
            # If Movie Exists in database
            # Just add movie to list
            # Else
            # Save Movie To Database and Add To List
            print("I Am Here")
            ##print(Movie.objects.get(imbd_id=x))
            
            #!!!!!!movie = Movie.objects.get(imbd_id=x)
            if Movie.objects.filter(imbd_id=x).count() == 0:                
                imbd_id = x
                
                API_KEY= "k_tx163xr6"
                    
                url = f'https://imdb-api.com/en/API/Title/{API_KEY}/{imbd_id}/FullActor,Posters,Images,Trailer,Ratings,Wikipedia,'
                    
                headers= {
                    "Authorization": f"Bearer {API_KEY}"
                }
                
                response = requests.get(url,headers=headers)
                data = response.json()
                #print(data)
                title = data['title']
                year = data['year']
                runtime= data['runtimeStr']
                rated = data['imDbRating']
                plot = data['plot']
                awards = data['awards']
                directors = data['directors']
                stars = data['stars']
                genres = data['genres']
                trailers = data['trailer']
                trailer = trailers['linkEmbed']
                #print(trailer)
                #print(trailer['link'])
                #Fix Trailer
                released= data['releaseDate']
                poster = data['image']
                
                #print(f'{title}  {year}  {runtime}  {rated} {plot} {awards} {directors} {stars} {genres} {released} {poster} ')

                movie = Movie.objects.create(imbd_id =imbd_id, title = title, year = year, Runtime= runtime, Plot = plot, Awards = awards, Directors = directors, Stars = stars, Genres = genres, Rating = rated, Trailer = trailer, Released = released, Poster = poster)
            else:     
                print("movie Already excists")
                movie = Movie.objects.get(imbd_id=x)

            list.movies.add(movie)
        # user = request.user
        # profile = Profile.objects.get(user=user)
        return redirect(search)
    
    #return redirect(search)
    #profile.watched.add(movie)
    #print("added" + f'movie')
    
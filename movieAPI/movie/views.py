from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from movie.forms import ListForm

from accounts.models import Profile
from movie.models import Movie, List

from django.db.models import Count
from django.contrib import messages


import requests
# Create your views here.
@login_required(login_url='index')
def search(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    lists = List.objects.filter(profile=profile).order_by('id').reverse()
    
    return render(request, 'search.html',{'lists':lists})

@login_required(login_url='index')
def results(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        listname= request.POST.get('list_name')
        print(listname)
        
        lists = List.objects.filter(profile=profile).order_by('id').reverse()
        
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

@login_required(login_url='index')
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
    
    
@login_required(login_url='index')
def addListName(request):
    form = ListForm(request.POST or None)
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    lists = List.objects.filter(profile=profile).order_by('id').reverse()
    
    #print(lists)
    
    if request.method == "POST":
        
        if form.is_valid():
            form.instance.profile = profile
            name = request.POST.get('name')

            if List.objects.filter(profile=profile).filter(name=name).count() != 0:
                messages.warning(request, 'You entered a List Name You have already!')
                context ={
                    'lists' :lists,
                    'profile':profile,
                    'form': form
                }
                #print(form.data.name)
                return render(request,'makeList.html', context) 
            else:
                form.save()
            
                messages.success(request, 'Successfully Added List!')

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
    
        


@login_required(login_url='index')
def addMoviesToList(request):
    user = request.user.id
    profile = Profile.objects.get(user__id = user)
    if request.method == "POST":
        movies = request.POST.getlist('movies')
        list_name = request.POST.get('list_name')
        print(list_name)
        print(List.objects.filter(profile=profile).count())
        if List.objects.filter(profile=profile).count() == 0:
            list = List.objects.create(profile = profile, name = 'My List 1')
        else:
            if list_name == 'None':  
                list = List.objects.filter(profile=profile).first()
            else:
                list = List.objects.filter(profile=profile).get(name=list_name)
            

        print("this is the list")
        print(list)
        
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
        messages.success(request, 'Successfully Added Movies!')

        return redirect(search)
    
    #return redirect(search)
    #profile.watched.add(movie)
    #print("added" + f'movie')
    
@login_required(login_url='index')
def editListView(request):
    #get list name, get user, get profile, render edit list page
    user = request.user.id
    profile = Profile.objects.get(user = user)
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        list=List.objects.filter(profile=profile).get(name=list_name)
        
        movies = list.movies.all()
        context = {
            
            'list_name':list_name,
            'list':movies,
            'profile':profile,
        }

        return render(request,'editList.html',context )
        
#get User/Profile, Get ListName and New List name from form
#get List, Update List name to new name, save
@login_required(login_url='index')
def updateListName(request):
    user=request.user.id
    profile=Profile.objects.get(user=user)
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        new_name = request.POST.get('new_list_name')
        list=List.objects.filter(profile=profile).get(name=list_name)
        list.name = new_name
        list.save()
        movies = list.movies.all()
        context={
            'list_name':new_name,
            'list': movies,
            'profile':profile,
        }        
        messages.success(request, 'Successfully Updated List Name From:'+ list_name + ' to: ' + new_name +' !')
        return render(request,'editList.html',context)
        
    
    

#Delete One Movie From List At a Time And Re Render The List
#Get User/Profile, Get List and ID from POST form
# Remove Movie from list, render page.
@login_required(login_url='index')
def deleteMovieFromList(request):
    user = request.user.id
    profile = Profile.objects.get(user = user)
    
    if request.method == 'POST':
        #get list name, get movie id from form
        list_name = request.POST.get('list_name')
        movie_id= request.POST.get('imbd_id')
        #get list object, get movie object 
        list=List.objects.filter(profile=profile).get(name=list_name)
        movie = Movie.objects.get(imbd_id=movie_id)
        list.movies.remove(movie)
        movies = list.movies.all()
        
        context={
            'list_name':list_name,
            'list':movies,
            'profile':profile,
            
        }
        messages.warning(request, 'Successfully Deleted ' + movie.title +' from list ' + list_name + '!')

        return render(request, 'editList.html',context)
        
        
        
#Delete Entire List and Redirect to Profile
#Get User/Profile from Request, get Get List name from form
#Get List object and Delete From Database
@login_required(login_url='index')
def deleteList(request):
    user = request.user.id
    profile = Profile.objects.get(user = user)
    
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        list=List.objects.filter(profile=profile).get(name=list_name)
        list.delete()
        messages.warning(request, 'Successfully Deleted '  + list_name + '  !')

        return redirect('view_profile')
    
    return redirect('view_profile')
        
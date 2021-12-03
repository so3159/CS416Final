from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import requests
# Create your views here.
@login_required(login_url='login')
def index(request):
    
    return render(request, 'index.html')

def index2(request):
    
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
        
        return render(request,'index2.html',{
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
    
    
    
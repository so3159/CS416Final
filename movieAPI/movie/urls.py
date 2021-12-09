from django.urls import path
from . import views



urlpatterns = [
    path('search/', views.search, name='search'),
    path('results/',views.results, name='results'),
    path('details/<id>', views.movieDetails, name='movieDetails'),
    path('addMoviesToList/', views.addMoviesToList, name='addMoviesToList'),
    path('addListName/', views.addListName, name="addListName"),
    path('editList/' , views.editListView, name='editListView'),
    path('deleteMovie/', views.deleteMovieFromList, name='deleteMovieFromList'),
    path('editListName/', views.updateListName, name='updateListName'),
    path('deleteList/', views.deleteList, name="deleteList")
]

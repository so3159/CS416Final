from typing import List
from django.contrib import admin
from .models import Movie
from movie.models import List
# Register your models here.

admin.site.register(Movie)
admin.site.register(List)
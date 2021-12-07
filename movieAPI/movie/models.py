from django.db import models


from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.

#movie Model
class Movie(models.Model):
    
    imbd_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=25, blank=True)
    Runtime = models.CharField(max_length=25, blank=True)
    Plot = models.TextField(blank=True)
    Awards= models.CharField(max_length=75, blank=True)
    Directors= models.CharField(max_length=50, blank=True)
    Stars = models.CharField(max_length=50, blank=True)
    Genres = models.CharField(max_length=50, blank=True)
    Rating = models.CharField(max_length=10, blank = True)
    Trailer= models.CharField(max_length=100, blank = True)
    Released = models.CharField(max_length=25, blank=True)
    Poster= models.ImageField(upload_to='movies', blank=True)
    #should a foreign Key of list Go in here?
    
    
    def __str__(self):
        return self.title
    
    


class List(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    movies = models.ManyToManyField(Movie, blank=True)
    
    def __str__(self):
        if self.name==None:
            return ''
        
        return self.name

#Director Model

# If you do not want symmetry in many-to-many relationships with self, set symmetrical to False.
# This will force Django to add the descriptor for the reverse relationship, allowing ManyToManyField
# relationships to be non-symmetrical.
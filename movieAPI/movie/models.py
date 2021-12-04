from django.db import models


from django.contrib.auth.models import User
# Create your models here.

#movie Model
class Movie(models.Model):
    
    imbd_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=25, blank=True)
    Runtime = models.CharField(max_length=25, blank=True)
    Rated = models.CharField(max_length=10, blank=True)
    Released = models.CharField(max_length=25, blank=True)
    Poster= models.ImageField(upload_to='movies', blank=True)
    
    def __str__(self):
        return self.Title
    
    
#Actor Model

#Director Model


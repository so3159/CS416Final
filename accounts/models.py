from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

#from movie.models import Movie, List

from django.db.models.fields.files import ImageField 

# Create your models here.


#Profile Model

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    #lists = models.ForeignKey(List, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return super().__str__()
    

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
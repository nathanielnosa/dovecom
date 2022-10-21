from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    fullname = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    profile_pix = models.ImageField(upload_to="profiles/", default='avartarone.jpg')
    
    def __str__(self):
        return self.fullname

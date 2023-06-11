from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Unknown")
    description = models.TextField()
    def __str__(self):
        return self.name

class Itinerary(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    destination = models.ForeignKey(Destination,on_delete=models.SET_DEFAULT, default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    class Meta:
        app_label = 'pages'
        
    def __str__(self):
        return self.title

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=100)

    def __str__(self):
        return self.name




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
